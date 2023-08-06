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

import numpy as np
import pandas as pd
from ibm_metrics_plugin.common.utils.constants import ProblemType
from ibm_metrics_plugin.common.utils.metrics_logger import MetricLogger
from ibm_metrics_plugin.metrics.drift_v2.entity.accuracy.meta_model import \
    MetaModel
from ibm_metrics_plugin.metrics.drift_v2.entity.column.categorical_column import \
    CategoricalColumn
from ibm_metrics_plugin.metrics.drift_v2.entity.column.data_column import \
    DataColumn
from ibm_metrics_plugin.metrics.drift_v2.entity.column.numerical_column import \
    NumericalColumn
from ibm_metrics_plugin.metrics.drift_v2.entity.column.probability_column import \
    ProbabilityColumn
from ibm_metrics_plugin.metrics.drift_v2.entity.dataset.data_set import \
    DriftDataSet
from ibm_metrics_plugin.metrics.drift_v2.utils.constants import (
    META_MODEL_TARGET_COLUMN, PROBABILITY_COLUMN_TEMPLATE, ColumnRole,
    DataSetType, PredictionClassification)
from ibm_metrics_plugin.metrics.drift_v2.utils.control_box import \
    ControlBoxManager
from ibm_metrics_plugin.metrics.drift_v2.utils.drift_utils import \
    get_logging_params
from tqdm import tqdm

logger = MetricLogger(__name__)


class PandasDataSet(DriftDataSet):

    def __init__(self, data_set_type: DataSetType) -> None:
        super().__init__(data_set_type)

    async def initialize(self,
                         data: pd.DataFrame,
                         problem_type: ProblemType,
                         feature_columns: List[str],
                         feature_importance: dict,
                         categorical_columns: List[str] = [],
                         label_column: str = None,
                         prediction_column: str = None,
                         probability_column: str = None,
                         max_samples: int = None,
                         score_fn: callable = None,
                         config_map: dict = {}):
        """Initialize the dataset with columns, operations etc.

        Args:
            data (pd.DataFrame): The data to initialize the dataset with.
            problem_type (ProblemType): The problem type of the dataset.
            feature_columns (List[str]): The list of feature columns.
            feature_importance (dict): The feature importance dictionary.
            categorical_columns (List[str], optional): The list of categorical columns. Defaults to [].
            label_column (str, optional): The label column. Defaults to None.
            prediction_column (str, optional): The prediction column. Defaults to None.
            probability_column (str, optional): The probability column. Defaults to None.
            score_fn (callable, optional): The scoring function. Accepts a dataframe with features as
                columns and returns a tuple of numpy array of probabilities array of shape `(n_samples,n_classes)`
                and numpy array of prediction vector of shape `(n_samples,)`. Defaults to None.
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

        self.count = len(data)
        if (max_samples is not None) and (max_samples <= self.count):
            data = data.sample(n=self.max_samples)
            self.count = max_samples

        total_columns = len(feature_columns)
        total_columns += 1 if label_column is not None else 0
        total_columns += 1 if prediction_column is not None else 0

        tqdm_bar = tqdm(
            total=total_columns,
            desc="Analyzing columns...",
            file=sys.stdout,
            unit="columns",
            dynamic_ncols=True,
            disable=not(
                ControlBoxManager().get_control_box().get_show_progress_bar()))

        for column in feature_columns:
            if column in categorical_columns:
                data_column = CategoricalColumn(column, role=ColumnRole.CATEGORICAL)
            else:
                data_column = NumericalColumn(column, role=ColumnRole.FEATURE)

            self.add_column(data_column)
            await data_column.compute_stats(data)
            logger.log_info(
                "Feature Column added to the data set.",
                get_logging_params(
                    column=column))
            tqdm_bar.update()

        if label_column is not None:
            data_column = CategoricalColumn(
                label_column,
                role=ColumnRole.LABEL) if self.data_schema[label_column] in (
                "str",
                "bool") else NumericalColumn(
                label_column,
                role=ColumnRole.LABEL)

            self.add_column(data_column)
            await data_column.compute_stats(data)
            logger.log_info(
                "Label Column added to the data set.",
                get_logging_params(
                    column=label_column))
            tqdm_bar.update()

            if self.problem_type is not ProblemType.REGRESSION:
                self.unique_labels = list(data[label_column].unique())

        # Score the data if:
        # 1. score_fn is not None
        # 2. prediction_column is not None and is not in the schema. (Only for regression)
        # 3. prediction_column and probability_column are not None and are not in
        # the schema. (Only for classification)

        if (self.problem_type is ProblemType.REGRESSION) and (
                prediction_column not in self.data_schema):
            self.score_data(score_fn, data, prediction_column)

        elif (prediction_column not in self.data_schema or probability_column not in self.data_schema):
            self.score_data(score_fn, data, prediction_column, probability_column)

        if (prediction_column is not None):
            data_column = CategoricalColumn(
                prediction_column,
                role=ColumnRole.PREDICTION) if self.data_schema[prediction_column] in (
                "str",
                "bool") else NumericalColumn(
                prediction_column,
                role=ColumnRole.PREDICTION)

            self.add_column(data_column)
            await data_column.compute_stats(data)
            logger.log_info(
                "Prediction Column added to the data set.",
                get_logging_params(
                    column=prediction_column))
            tqdm_bar.update()

        if problem_type in (ProblemType.BINARY, ProblemType.MULTICLASS):
            if probability_column is not None:
                data_column = DataColumn(probability_column, role=ColumnRole.PROBABILITY_VECTOR)

                self.add_column(data_column)

                await self.add_individual_probability_columns(
                    prediction_column, probability_column, data, tqdm_bar)

            accuracy_drift_flag = ControlBoxManager().get_control_box().get_enable_accuracy_drift()
            if accuracy_drift_flag:

                if data[label_column].dtype == "object":
                    target_values = np.where(
                        data[prediction_column].str.lower() == data[label_column].str.lower(),
                        PredictionClassification.CORRECT.value,
                        PredictionClassification.INCORRECT.value)
                else:
                    target_values = np.where(
                        data[prediction_column] == data[label_column],
                        PredictionClassification.CORRECT.value,
                        PredictionClassification.INCORRECT.value)

                data = data.assign(**{META_MODEL_TARGET_COLUMN: target_values})
                self.meta_model = MetaModel.factory(data, data_set=self)

                if len(self.meta_model.errors_map) == 0:
                    self.has_accuracy_drift = True
                    data_column = CategoricalColumn(
                        META_MODEL_TARGET_COLUMN, role=ColumnRole.META_MODEL_TARGET)
                    self.add_column(data_column)
                    self.data_schema.update({data_column.name: "string"})
                    # Compute accuracy drift insights

                else:
                    logger.log_warning(
                        f"Got the following errors while training meta model: {self.meta_model.errors_map}",
                        get_logging_params(
                            data_set=self))

        tqdm_bar.close()

        await self.add_single_operations(data=data)
        await self.add_two_column_operations(data=data)
        await self.add_data_quality_issues(data=data)
        logger.log_info(
            "Initialized the data set.",
            get_logging_params(
                data_set=self,
                start_time=start_time))

    def score_data(
            self,
            score_fn: callable,
            data: pd.DataFrame,
            prediction_column: str,
            probability_column: str = None):

        start_time = time()
        if self.problem_type is ProblemType.REGRESSION:
            data[prediction_column] = self._split_and_score(score_fn, data)
            self.data_schema = {
                **self.data_schema,
                prediction_column: self.convert_column_dtypes_to_native(
                    data[prediction_column].dtype)}
        else:
            result = self._split_and_score(score_fn, data)
            data[prediction_column] = result[0]
            self.data_schema = {
                **self.data_schema,
                prediction_column: self.convert_column_dtypes_to_native(
                    data[prediction_column].dtype)}
            data[probability_column] = result[1].tolist()
            self.data_schema = {
                **self.data_schema,
                prediction_column: self.convert_column_dtypes_to_native(
                    data[prediction_column].dtype)}
        logger.log_info(
            f"Scored {len(data)} rows.",
            get_logging_params(
                data_set=self,
                start_time=start_time))

    def get_data_schema(self, data: pd.DataFrame) -> Dict[str, str]:
        """Get the data schema.

        Args:
            data (pd.DataFrame): The data to get the schema from.

        Returns:
            Dict[str, str]: The schema of the table. The keys are the column names
                and the values are the column types
        """
        result = data.dtypes.astype("str").to_dict()
        result = {col: self.convert_column_dtypes_to_native(
            dtype) for col, dtype in result.items()}

        return result

    def _validate_score_probabilities(
            self,
            probabilities: np.ndarray,
            expected_rows: int) -> np.ndarray:
        """Validate the probabilities array from the score function.

        Args:
            probabilities (np.ndarray): The probabilities array.
            expected_rows (int): The expected number of rows.

        Raises:
            ValueError: Raises this exception in the following cases:
                1. The probabilities array is not of type numpy.ndarray.
                2. The probabilities array is not of shape `(expected_rows,n_classes)`.
                3. The values in the probabilities array can not be cast to float type.
                4. The values in the probabilities array are not between 0 and 1 (both inclusive).

        Returns:
            np.ndarray: The probabilities array.
        """
        # 1. Validate if probabilities is a numpy array of shape (expected_rows, classes)
        if not(isinstance(probabilities, np.ndarray)):
            raise ValueError(
                "The probabilities output is not of type numpy.ndarray.")

        expected_shape = (expected_rows, self.get_label_column().distinct_count)
        if probabilities.shape != expected_shape:
            raise ValueError(
                f"The shape of probabilities output is \"{probabilities.shape}\" but should be {expected_shape}.")

        # 2. Try to convert probabilities to float
        try:
            probabilities = probabilities.astype(float)
        except Exception as e:
            raise ValueError(
                f"The probabilities output is of type \"{probabilities.dtype.name}\" which can not be cast to float.") from e

        # 3. Validate that all values of probabilities fall between 0 and 1 inclusive.
        if not(np.all(probabilities >= 0)) and not(np.all(probabilities <= 1)):
            raise ValueError(
                "The probabilities output does not lie between 0 and 1.")

        return probabilities

    def _validate_score_predictions(self, predictions: np.ndarray,
                                    expected_rows: int) -> np.ndarray:
        """Validate the predictions array from the score function.

        Args:
            predictions (np.ndarray): The predictions array.
            expected_rows (int): The expected number of rows.

        Raises:
            ValueError: Raises this exception in the following cases:
                1. The predictions array is not of type numpy.ndarray.
                2. The predictions array is not of shape `(expected_rows,)`.
                3. The values in the predictions array can not be cast to the
                same data type as the label column.
                4. For classification problems, the values in the predictions array
                are not same as the values of the label column.

        Returns:
            np.ndarray: The predictions array.
        """
        # 1. Validate if predictions is a numpy array of shape (batch_size, )
        if not(isinstance(predictions, np.ndarray)):
            raise ValueError(
                f"The predictions output is of {type(predictions)} type. It should be of type numpy.ndarray.")

        expected_shape = (expected_rows, )
        if predictions.shape != expected_shape:
            raise ValueError(
                f"The shape of predictions output is {predictions.shape} but should be {expected_shape}")

        # 2. Try to cast them in same dtype as label column
        label_column = self.get_label_column()
        predictions_dtype = predictions.dtype.name
        try:
            predictions = predictions.astype(label_column.data_type)
        except Exception as e:
            raise ValueError(
                f"The predictions output is of type \"{predictions_dtype}\" and can not be cast to data type \"{label_column.data_type}\" of the label column.") from e

        if self.problem_type is not ProblemType.REGRESSION:
            predicted_classes = np.unique(predictions)

            # Check if any value in prediction vector is not present in
            # training data class names. We are now doing string based comparison after
            # converting training labels and predicted classes to lowercase
            if label_column.data_type == "str":
                temp_predicted_classes = list(
                    map(str.lower, map(str, predicted_classes)))
                training_labels = list(
                    map(str.lower, map(str, self.unique_labels)))
            else:
                temp_predicted_classes = predicted_classes
                training_labels = self.unique_labels
            if any(prediction not in training_labels for prediction in temp_predicted_classes):
                raise ValueError(
                    f"The model predictions \"{predicted_classes}\" are different from values in label column \"{self.unique_labels}\"")

        return predictions

    def _split_and_score(self, score, input_df):
        """Splits the input dataframe into chunks of data dictated by
        `batch_size` and scores using `score` param.


        Arguments:
            score {function} -- function to score
            input_df {pandas.DataFrame} -- dataframe

        Returns:
            tuple -- probabilities and predictions for entire dataframe
        """
        probabilities = []
        predictions = []

        batch_size = ControlBoxManager().get_control_box().get_model_score_batch_size()
        start = 0
        end = min(batch_size, len(input_df))

        tqdm_bar = tqdm(
            total=len(input_df),
            desc="Scoring dataframe...",
            file=sys.stdout,
            unit="rows",
            dynamic_ncols=True,
            disable=not(
                ControlBoxManager().get_control_box().get_show_progress_bar()))

        while start < len(input_df):
            start_time = time()
            if self.problem_type is ProblemType.REGRESSION:
                prediction_vector = score(input_df.iloc[start:end])
                prediction_vector = self._validate_score_predictions(prediction_vector, end - start)
                predictions.append(prediction_vector)
            else:
                probabilities_vector, prediction_vector = score(input_df.iloc[start:end])
                probabilities_vector = self._validate_score_probabilities(
                    probabilities_vector, end - start)
                probabilities.append(probabilities_vector)
                prediction_vector = self._validate_score_predictions(prediction_vector, end - start)
                predictions.append(prediction_vector)

            tqdm_bar.update(n=(end - start))
            start = end
            end = min(start + batch_size, len(input_df))
            logger.log_debug(
                f"Scored {start}/{len(input_df)} rows.",
                get_logging_params(
                    data_set=self,
                    start_time=start_time))

        tqdm_bar.close()

        if self.problem_type is ProblemType.REGRESSION:
            return np.concatenate(predictions)

        return np.concatenate(predictions), np.concatenate(probabilities)

    async def add_individual_probability_columns(
            self,
            prediction_column: str,
            probability_column: str,
            data: pd.DataFrame,
            tqdm_bar) -> pd.DataFrame:
        # 1. Check if probability column has arrays/lists or strings
        # If string, then we need to convert to list
        is_probability_list = data[probability_column].apply(
            lambda x: isinstance(x, (list, np.ndarray))).all()
        is_probability_str = data[probability_column].apply(lambda x: isinstance(x, (str))).all()

        if not is_probability_list and not is_probability_str:
            raise ValueError(
                f"Column {probability_column} is not a list or a string. {data[probability_column].dtype}")

        if is_probability_str:
            data[probability_column] = data[probability_column].apply(
                lambda x: list(map(float, x.split(","))))

        self.predicted_labels = self.get_predicted_labels(
            prediction_column, probability_column, data)
        tqdm_bar.total += len(self.predicted_labels)

        class_probability_columns = [
            PROBABILITY_COLUMN_TEMPLATE.substitute(
                prediction=label) for label in self.predicted_labels]
        data[class_probability_columns] = pd.DataFrame(
            data[probability_column].values.tolist(), index=data.index)

        for prediction in self.predicted_labels:
            data_column = ProbabilityColumn(prediction)
            # Append the new class probability columns to the schema
            self.data_schema.update({data_column.name: "float"})

            self.add_column(data_column)
            await data_column.compute_stats(data)
            logger.log_info(
                "Probability Column added to the data set.",
                get_logging_params(
                    column=data_column))
            tqdm_bar.update()

    def get_predicted_labels(
            self,
            prediction_column: str,
            probability_column: str,
            data: pd.DataFrame) -> List[str]:
        """Arrange the predicted labels in the order of the probabilities array.

        Args:
            prediction_column (str): Name of the prediction column.
            probability_column (str): Name of the probability column.
            data (pd.DataFrame): Dataframe containing the prediction and probability columns.

        Raises:
            Exception: If not able to get the predicted labels.

        Returns:
            List[str]: List of predicted labels.
        """

        predicted_labels = [None] * len(self.unique_labels)

        for prediction, probability in zip(data[prediction_column], data[probability_column]):
            max_index = np.argwhere(
                probability == np.amax(probability)).flatten()
            if len(max_index) > 1:
                continue

            if prediction not in predicted_labels:
                predicted_labels[max_index[0]] = prediction

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
