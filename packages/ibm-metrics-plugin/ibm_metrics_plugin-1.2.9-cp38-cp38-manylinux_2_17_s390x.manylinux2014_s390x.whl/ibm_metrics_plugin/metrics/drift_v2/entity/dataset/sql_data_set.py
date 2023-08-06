# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2022
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

import sys
from time import time
from typing import Dict, List

import pandas as pd
import sqlalchemy
from ibm_metrics_plugin.clients.readers.async_query_executor import \
    execute_count_query
from ibm_metrics_plugin.common.utils.constants import ProblemType
from ibm_metrics_plugin.common.utils.metrics_logger import MetricLogger
from ibm_metrics_plugin.metrics.drift_v2.entity.column.categorical_column import \
    CategoricalColumn
from ibm_metrics_plugin.metrics.drift_v2.entity.column.data_column import \
    DataColumn
from ibm_metrics_plugin.metrics.drift_v2.entity.column.numerical_column import \
    NumericalColumn
from ibm_metrics_plugin.metrics.drift_v2.entity.column.probability_column import \
    ProbabilityColumn
from ibm_metrics_plugin.metrics.drift_v2.entity.data_quality.data_quality_issue import \
    DataQualityIssue
from ibm_metrics_plugin.metrics.drift_v2.entity.dataset.data_set import \
    DriftDataSet
from ibm_metrics_plugin.metrics.drift_v2.entity.operation.operation import \
    Operation
from ibm_metrics_plugin.metrics.drift_v2.utils.async_utils import \
    gather_with_concurrency
from ibm_metrics_plugin.metrics.drift_v2.utils.constants import (ColumnRole,
                                                                 DataSetType)
from ibm_metrics_plugin.metrics.drift_v2.utils.control_box import \
    ControlBoxManager
from ibm_metrics_plugin.metrics.drift_v2.utils.drift_utils import \
    get_logging_params
from tqdm import tqdm

logger = MetricLogger(__name__)


class SqlDataSet(DriftDataSet):
    def __init__(self, data_set_type: DataSetType):
        super().__init__(data_set_type)
        self.schema_name = None
        self.table_name = None
        self._full_table_name = None

    @property
    def full_table_name(self) -> str:
        """Get the full table name

        Raises:
            Exception: If the schema name or the table name is not set

        Returns:
            str: The full table name
        """

        if self._full_table_name is not None:
            return self._full_table_name

        if self.schema_name is None or self.table_name is None:
            raise Exception("Schema and table are not set.")

        if self.max_samples is None:
            self._full_table_name =  f"\"{self.schema_name}\".\"{self.table_name}\""
        else:
            self._full_table_name = f"(SELECT * FROM \"{self.schema_name}\".\"{self.table_name}\" LIMIT {self.max_samples}) AS DATA_SET_SUB_QUERY "
        return self._full_table_name

    @property
    def count_query(self) -> str:
        """The query to count the number of rows in the table

        Returns:
            str: The query to count the number of rows in the table
        """
        return f"SELECT COUNT(*) FROM {self.full_table_name}"

    def distinct_values_query(self, column: str) -> str:
        """The query to get the distinct values of a column

        Args:
            column (str): The column name

        Returns:
            str: The query to get the distinct values of a column
        """
        return f"SELECT DISTINCT \"{column}\" FROM {self.full_table_name}"

    def probability_column_query(
            self,
            prediction_column: str,
            probability_column: str,
            prediction: str) -> str:
        """The query to get the probability column of a particular prediction in the prediction column

        Args:
            prediction_column (str): The prediction column name
            probability_column (str): The probability column name
            prediction (str): The prediction

        Returns:
            str: The query.
        """

        return f"SELECT \"{probability_column}\" FROM {self.full_table_name} WHERE \"{prediction_column}\" = '{prediction}' LIMIT 10"

    async def count_rows(self, data: sqlalchemy.engine.base.Engine) -> int:
        """Count the number of rows in the table

        Args:
            data (sqlalchemy.engine.base.Engine): The database connection

        Raises:
            Exception: If the query to count the number of rows in the table fails

        Returns:
            int: The number of rows in the table
        """
        count = await execute_count_query(query=self.count_query, data=data)
        return count

    def get_data_schema(self, data: sqlalchemy.engine.base.Engine) -> Dict[str, str]:
        """Get the data schema.

        Args:
            data (sqlalchemy.engine.base.Engine): The data to get the schema from.

        Raises:
            Exception: If the query to get the schema of the table fails

        Returns:
            Dict[str, str]: The schema of the table. The keys are the column names
                and the values are the column types
        """
        start_time = time()
        try:
            metadata = sqlalchemy.MetaData(bind=data, schema=self.schema_name)
            table = sqlalchemy.Table(self.table_name, metadata, autoload=True)
            schema = {column.name: str(column.type.python_type.__name__)
                      for column in table.columns}
            logger.log_info(
                f"Fetched schema. {schema}",
                get_logging_params(
                    data_set=self,
                    start_time=start_time))
            return schema

        except sqlalchemy.exc.SQLAlchemyError as e:
            raise Exception(
                f"Got an error while getting schema of the table {self.full_table_name}") from e

    def get_unique_labels(
            self,
            data: sqlalchemy.engine.base.Engine,
            label_column: str) -> List[str]:
        """Get the unique labels of the label column

        Args:
            data (sqlalchemy.engine.base.Engine): The database connection
            label_column (str): The label column name

        Raises:
            Exception: If the query to get the unique labels of the label column fails

        Returns:
            List[str]: The unique labels of the label column
        """

        start_time = time()
        query = self.distinct_values_query(label_column)
        try:
            with data.connect() as conn:
                logger.log_info(
                    "Executing query for unique values in {label_column}.",
                    get_logging_params(
                        data_set=self,
                        query=query))
                result = pd.read_sql(query, conn)
                logger.log_info(
                    "Executed query for unique values in {label_column}.",
                    get_logging_params(
                        data_set=self,
                        query=query,
                        start_time=start_time))
                return result[label_column].values

        except sqlalchemy.exc.SQLAlchemyError as e:
            raise Exception(
                f"Got an error while executing the query {query}") from e

    def get_distinct_predictions(self,
                                 data: sqlalchemy.engine.base.Engine,
                                 prediction_column: str) -> List[str]:
        """Get the unique predictions of the prediction column

        Args:
            data (sqlalchemy.engine.base.Engine): The database connection
            prediction_column (str): The prediction column name

        Raises:
            Exception: If the query to get the unique predictions of the prediction column fails

        Returns:
            List[str]: The unique predictions of the prediction column
        """

        start_time = time()
        query = self.distinct_values_query(prediction_column)
        try:
            with data.connect() as conn:
                logger.log_info(
                    "Executing query for unique values in {prediction_column}.",
                    get_logging_params(
                        data_set=self,
                        query=query))
                result = pd.read_sql(query, conn)
                logger.log_info(
                    "Executed query for unique values in {prediction_column}.",
                    get_logging_params(
                        data_set=self,
                        query=query,
                        start_time=start_time))
                return result[prediction_column].values

        except sqlalchemy.exc.SQLAlchemyError as e:
            raise Exception(
                f"Got an error while executing the query {query}") from e

    def get_probabilities(
            self,
            data: sqlalchemy.engine.base.Engine,
            prediction_column: str,
            probability_column: str,
            prediction: str) -> List[float]:
        """Get the probabilities of a particular prediction in the prediction column

        Raises:
            Exception: If the query to get the probabilities of a particular prediction in the prediction column fails

        Returns:
            List[float]: The probabilities of a particular prediction in the prediction column
        """
        start_time = time()
        query = self.probability_column_query(prediction_column, probability_column, prediction)
        try:
            with data.connect() as conn:
                logger.log_info(
                    "Executing query for fetching probabilities for {prediction_column}.",
                    get_logging_params(
                        data_set=self,
                        query=query))
                result = pd.read_sql(
                    query,
                    conn)
                logger.log_info(
                    "Executed query for fetching probabilities for {prediction_column}.",
                    get_logging_params(
                        data_set=self,
                        query=query,
                        start_time=start_time))

                if self.data_schema[probability_column] == "str":
                    # Convert the string probability column to expanded float values
                    result = result[probability_column].str.replace(
                        "[", "").str.replace(
                        "]", "").str.split(
                        ",", expand=True).astype(float)
                else:
                    result = pd.DataFrame(result[probability_column].tolist()).astype(float)
                return result

        except sqlalchemy.exc.SQLAlchemyError as e:
            raise Exception(
                f"Got an error while executing the query {query}") from e

    async def initialize(self,
                         data: dict,
                         problem_type: ProblemType,
                         feature_columns: List[str],
                         feature_importance: dict,
                         categorical_columns: List[str] = [],
                         label_column: str = None,
                         prediction_column: str = None,
                         probability_column: str = None,
                         max_samples: int = None,
                         score_fn: callable = None,
                         config_map: dict = None):
        """Initialize the dataset with columns, operations etc.

        Args:
            data (dict): The data to initialize the dataset with.
            problem_type (ProblemType): The problem type of the dataset.
            feature_columns (List[str]): The list of feature columns.
            feature_importance (dict): The feature importance dictionary.
            categorical_columns (List[str], optional): The list of categorical columns. Defaults to [].
            label_column (str, optional): The label column. Defaults to None.
            prediction_column (str, optional): The prediction column. Defaults to None.
            probability_column (str, optional): The probability column. Defaults to None.

        """

        start_time = time()
        self.set_control_box(config_map=config_map)

        self.validate_data(data=data,
                           feature_columns=feature_columns,
                           categorical_columns=categorical_columns,
                           feature_importance=feature_importance,
                           label_column=label_column,
                           prediction_column=prediction_column,
                           probability_column=probability_column,
                           score_fn=score_fn)

        self.problem_type = problem_type
        self.max_samples = max_samples
        self.set_feature_importance(feature_importance)

        data = DriftDataSet.convert_to_engine(data)
        self.dialect = data.dialect.name
        self.count = await self.count_rows(data)

        total_columns = len(feature_columns)
        total_columns += 1 if label_column is not None else 0
        total_columns += 1 if prediction_column is not None else 0

        # tqdm_bar = tqdm(
        #     total=total_columns,
        #     desc="Analyzing columns...",
        #     file=sys.stdout,
        #     unit="columns",
        #     dynamic_ncols=True,
        #     disable=not(
        #         ControlBoxManager().get_control_box().get_show_progress_bar()))

        column_tasks = []
        for column in feature_columns:
            if column in categorical_columns:
                data_column = CategoricalColumn(column, role=ColumnRole.CATEGORICAL)
            else:
                data_column = NumericalColumn(column, role=ColumnRole.FEATURE)

            self.add_column(data_column)
            column_tasks.append(data_column.compute_stats(data))
            # logger.log_info(
            #     "Feature Column added to the data set.",
            #     get_logging_params(
            #         column=column))
            # tqdm_bar.update()

        if label_column is not None:
            if self.problem_type is not ProblemType.REGRESSION:
                self.unique_labels = self.get_unique_labels(data, label_column)

            data_column = CategoricalColumn(
                label_column,
                role=ColumnRole.LABEL) if self.data_schema[label_column] in (
                "str",
                "bool") else NumericalColumn(
                label_column,
                role=ColumnRole.LABEL)

            self.add_column(data_column)
            column_tasks.append(data_column.compute_stats(data))
            # logger.log_info(
            #     "Label Column added to the data set.",
            #     get_logging_params(
            #         column=label_column))
            # tqdm_bar.update()

        if prediction_column is not None:
            data_column = CategoricalColumn(
                prediction_column,
                role=ColumnRole.PREDICTION) if self.data_schema[prediction_column] in (
                "str",
                "bool") else NumericalColumn(
                prediction_column,
                role=ColumnRole.PREDICTION)

            self.add_column(data_column)
            column_tasks.append(data_column.compute_stats(data))
            # logger.log_info(
            #     "Prediction Column added to the data set.",
            #     get_logging_params(
            #         column=prediction_column))
            # tqdm_bar.update()

        if (self.problem_type is not ProblemType.REGRESSION) and (probability_column is not None):
            data_column = DataColumn(probability_column, role=ColumnRole.PROBABILITY_VECTOR)
            self.add_column(data_column)
            # 1. Get index of every prediction in probability_column
            # a. Fetch 10 rows for each different prediction
            # b. Get the index of the prediction in the row
            # 2. Fetch each probability column separately and add it to dataset

            self.predicted_labels = self.get_predicted_labels(
                prediction_column, probability_column, data)
            # tqdm_bar.total += len(self.predicted_labels)

            for prediction in self.predicted_labels:
                data_column = ProbabilityColumn(prediction)
                data_column.set_probability_column(probability_column)
                data_column.set_predicted_labels(self.predicted_labels)
                # Append the new class probability columns to the schema
                self.data_schema.update({data_column.name: "float"})

                self.add_column(data_column)
                column_tasks.append(data_column.compute_stats(data))
                logger.log_info(
                    "Probability Column added to the data set.",
                    get_logging_params(
                        column=prediction_column))
                # tqdm_bar.update()
        # tqdm_bar.close()
        await gather_with_concurrency(*column_tasks)

        await self.add_single_operations(data=data)
        await self.add_two_column_operations(data=data)
        await self.add_data_quality_issues(data=data)
        logger.log_info(
            "Initialized the data set.",
            get_logging_params(
                data_set=self,
                start_time=start_time))

    def validate_predictions(self, predictions: List[str]) -> None:
        """Validate the predictions against the unique labels in the dataset

        Args:
            predictions (List[str]): The list of predictions to validate

        Raises:
            ValueError: If the predictions are different from the unique labels in the dataset
        """

        # Check if any value in prediction vector is not present in
        # training data class names. We are now doing string based comparison after
        # converting training labels and predicted classes to lowercase
        label_column = self.get_label_column()
        if label_column.data_type == "str":
            temp_predictions = list(
                map(str.lower, map(str, predictions)))
            training_labels = list(
                map(str.lower, map(str, self.unique_labels)))
        else:
            temp_predictions = predictions
            training_labels = self.unique_labels
        if any(prediction not in training_labels for prediction in temp_predictions):
            raise ValueError(
                f"The model predictions \"{predictions}\" are different from values in label column \"{self.unique_labels}\"")

        if any(label not in temp_predictions for label in training_labels):
            raise ValueError(
                f"The training labels \"{self.unique_labels}\" are different from values in prediction column \"{predictions}\"")

    def get_predicted_labels(
            self,
            prediction_column: str,
            probability_column: str,
            data: sqlalchemy.engine.base.Engine) -> List[str]:
        """Arrange the predicted labels in the order of the probabilities array.

        Args:
            prediction_column (str): Name of the prediction column.
            probability_column (str): Name of the probability column.
            data (sqlalchemy.engine.base.Engine): Data containing the prediction and probability columns.

        Raises:
            Exception: If not able to get the predicted labels.

        Returns:
            List[str]: List of predicted labels.
        """

        distinct_predictions = self.get_distinct_predictions(data, prediction_column)

        self.validate_predictions(distinct_predictions)

        predicted_labels = [None] * len(self.unique_labels)

        for prediction in distinct_predictions:
            probabilities = self.get_probabilities(
                data, prediction_column, probability_column, prediction)

            # Get index of the prediction in the probability vector for each row
            result = probabilities.idxmax(axis=1)

            # Pick the index occurring the maximum times
            prediction_index = result.value_counts().index[0]

            predicted_labels[prediction_index] = prediction

            empty_values = sum([label is None for label in predicted_labels])

            if empty_values == 1:
                idx = predicted_labels.index(None)
                label = (set(self.unique_labels) -
                         set(predicted_labels)).pop()
                predicted_labels[idx] = label
                break

        if sum([label is None for label in predicted_labels]) > 0:
            # TODO: Handle this case. Perhaps only have columns that are predicted
            raise Exception(f"Could not predict all the values for {probability_column}")

        return predicted_labels
