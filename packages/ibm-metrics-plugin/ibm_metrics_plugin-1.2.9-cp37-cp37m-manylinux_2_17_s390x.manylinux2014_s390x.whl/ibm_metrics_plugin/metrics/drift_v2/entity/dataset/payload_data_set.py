# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2022
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

import sys
from datetime import datetime
from time import time

import sqlalchemy
from ibm_metrics_plugin.common.utils.constants import ProblemType
from ibm_metrics_plugin.common.utils.metrics_logger import MetricLogger
from ibm_metrics_plugin.common.utils.python_utils import get_python_types
from ibm_metrics_plugin.metrics.drift_v2.entity.column.data_column import \
    DataColumn
from ibm_metrics_plugin.metrics.drift_v2.entity.column.meta_model_classification_column import \
    MetaModelClassificationColumn
from ibm_metrics_plugin.metrics.drift_v2.entity.column.meta_model_confidence_column import \
    MetaModelConfidenceColumn
from ibm_metrics_plugin.metrics.drift_v2.entity.data_quality.data_quality_issue import \
    DataQualityIssue
from ibm_metrics_plugin.metrics.drift_v2.entity.dataset.data_set import \
    DriftDataSet
from ibm_metrics_plugin.metrics.drift_v2.entity.dataset.sql_data_set import \
    SqlDataSet
from ibm_metrics_plugin.metrics.drift_v2.entity.operation.operation import \
    Operation
from ibm_metrics_plugin.metrics.drift_v2.utils.async_utils import \
    gather_with_concurrency
from ibm_metrics_plugin.metrics.drift_v2.utils.constants import (
    TIMESTAMP_FORMAT, ColumnRole, DataSetType)
from ibm_metrics_plugin.metrics.drift_v2.utils.control_box import \
    ControlBoxManager
from ibm_metrics_plugin.metrics.drift_v2.utils.drift_utils import \
    get_logging_params
from tqdm import tqdm

logger = MetricLogger(__name__)


class PayloadDataSet(SqlDataSet):
    def __init__(self):
        super().__init__(DataSetType.PRODUCTION)
        self.record_id_column = None
        self.record_timestamp_column = None
        self.start_timestamp = None
        self.end_timestamp = None

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

        limit_sub_clause = f" LIMIT {self.max_samples} " if self.max_samples is not None else ""

        where_clauses = []
        where_sub_clause = ""

        if self.start_timestamp is not None:
            self.start_timestamp = self.start_timestamp.strftime(TIMESTAMP_FORMAT)
            where_clauses.append(f"\"{self.record_timestamp_column}\" >= '{self.start_timestamp}'")
        if self.end_timestamp is not None:
            self.end_timestamp = self.end_timestamp.strftime(TIMESTAMP_FORMAT)
            where_clauses.append(f"\"{self.record_timestamp_column}\" <= '{self.end_timestamp}'")

        if where_clauses:
            where_sub_clause = f" WHERE " + " AND ".join(where_clauses)

        if limit_sub_clause or where_sub_clause:
            self._full_table_name = f"(SELECT * FROM \"{self.schema_name}\".\"{self.table_name}\" {where_sub_clause} {limit_sub_clause}) AS DATASET_SUB_QUERY"
        else:
            self._full_table_name = f"\"{self.schema_name}\".\"{self.table_name}\""

        return self._full_table_name

    @property
    def count_query(self) -> str:
        """The query to count the number of rows in the table

        Returns:
            str: The query to count the number of rows in the table
        """

        query = f"SELECT COUNT(*) FROM {self.full_table_name}"
        return query

    async def initialize(self,
                         data: dict,
                         baseline_data_set: DriftDataSet,
                         monitoring_run_id: str,
                         record_id_column: str,
                         record_timestamp_column: str,
                         start_timestamp: datetime,
                         end_timestamp: datetime,
                         max_samples: int):
        start_time = time()

        self.set_control_box(config_map=baseline_data_set.config_map)
        self.id = monitoring_run_id
        self.problem_type = baseline_data_set.problem_type
        self.max_samples = max_samples

        if self.problem_type in (ProblemType.BINARY, ProblemType.MULTICLASS):
            self.unique_labels = baseline_data_set.unique_labels
            self.predicted_labels = baseline_data_set.predicted_labels
        feature_columns = baseline_data_set.get_feature_columns()
        categorical_columns = baseline_data_set.get_categorical_columns()
        prediction_column = baseline_data_set.get_prediction_column().name
        probability_column = None

        if self.problem_type in (ProblemType.BINARY, ProblemType.MULTICLASS):
            probability_column = baseline_data_set.get_probability_column().name

        self.validate_data(data=data,
                           feature_columns=[column.name for column in feature_columns],
                           categorical_columns=[column.name for column in categorical_columns],
                           prediction_column=prediction_column,
                           probability_column=probability_column,
                           record_id_column=record_id_column,
                           record_timestamp_column=record_timestamp_column,
                           start_timestamp=start_timestamp,
                           end_timestamp=end_timestamp)

        self.set_feature_importance(baseline_data_set.feature_importance)
        self.record_id_column = record_id_column
        self.record_timestamp_column = record_timestamp_column
        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp

        data = DriftDataSet.convert_to_engine(data)
        # TODO Get start and end timestamps if they are none via query. And fill
        # proper values. Need to put them in measurements

        self.count = await self.count_rows(data)
        self.dialect = data.dialect.name

        await self.add_baseline_columns(baseline_data_set=baseline_data_set, data=data)

        await self.add_baseline_operations(baseline_data_set=baseline_data_set, data=data)

        await self.add_accuracy_drift_columns_operations(baseline_data_set=baseline_data_set, data=data)

        await self.add_data_quality_violations(baseline_data_set=baseline_data_set, data=data)

        logger.log_info(
            "Initialized the data set.",
            get_logging_params(
                data_set=self,
                start_time=start_time))

    async def add_baseline_columns(self, baseline_data_set: DriftDataSet,
                                   data: sqlalchemy.engine.base.Engine) -> None:
        # tqdm_bar = tqdm(
        #     total=len(baseline_data_set.columns),
        #     desc="Analyzing columns...",
        #     file=sys.stdout,
        #     unit="columns",
        #     dynamic_ncols=True,
        #     disable=not(
        #         ControlBoxManager().get_control_box().get_show_progress_bar()))

        column_tasks = []
        for baseline_column in baseline_data_set.columns.values():
            if baseline_column.role in (ColumnRole.LABEL, ColumnRole.META_MODEL_TARGET):
                continue
            data_column = DataColumn.copy_from(other=baseline_column)
            self.add_column(data_column)
            column_tasks.append(data_column.compute_stats(data))
            # logger.log_info("Column added to the data set.", get_logging_params(column=data_column))
            # tqdm_bar.update()

        await gather_with_concurrency(*column_tasks)
        # tqdm_bar.close()

    async def add_baseline_operations(self, baseline_data_set: DriftDataSet,
                                      data: sqlalchemy.engine.base.Engine) -> None:
        # tqdm_bar = tqdm(
        #     total=len(baseline_data_set.operations),
        #     desc="Analyzing operations...",
        #     file=sys.stdout,
        #     unit="operations",
        #     dynamic_ncols=True,
        #     disable=not(
        #         ControlBoxManager().get_control_box().get_show_progress_bar()))

        operation_tasks = []
        for baseline_operation in baseline_data_set.operations.values():
            if baseline_operation.target_column.role in (
                    ColumnRole.LABEL, ColumnRole.META_MODEL_TARGET):
                continue
            operation = Operation.copy_from(other=baseline_operation)
            operation.target_column = self.get_column(baseline_operation.target_column.name)

            if baseline_operation.source_column:
                if baseline_operation.source_column.role in (
                        ColumnRole.LABEL, ColumnRole.META_MODEL_TARGET):
                    continue
                operation.source_column = self.get_column(baseline_operation.source_column.name)

            self.add_operation(operation)
            operation_tasks.append(operation.execute(data))
            # logger.log_info(
            #     "Operation added to the data set.",
            #     get_logging_params(
            #         operation=operation))

            # tqdm_bar.update()
        await gather_with_concurrency(*operation_tasks)
        # tqdm_bar.close()

    async def add_accuracy_drift_columns_operations(
            self,
            baseline_data_set: DriftDataSet,
            data: sqlalchemy.engine.base.Engine) -> None:
        if not baseline_data_set.has_accuracy_drift:
            logger.log_info("Data set does not have accuracy drift enabled",
                            get_logging_params(data_set=baseline_data_set))
            return

        # Add drift model confidence
        data_column = MetaModelConfidenceColumn()
        self.add_column(data_column)
        self.data_schema.update({data_column.name: "float"})
        data_column.bin_width = 0.01

        operation = Operation.factory(target_column=data_column)
        self.add_operation(operation)
        await operation.execute(data)

        data_column = MetaModelClassificationColumn()
        self.add_column(data_column)
        self.data_schema.update({data_column.name: "string"})

        operation = Operation.factory(target_column=data_column)
        self.add_operation(operation)
        await operation.execute(data)

        operation_tasks = []
        for source_column, target_column in self.get_insights_columns(source_column=data_column):
            operation = Operation.factory(target_column=target_column, source_column=source_column)
            self.add_operation(operation)
            operation_tasks.append(operation.execute(data))
            # logger.log_info(
            #     "Two Column Operation added to the data set.",
            #     get_logging_params(
            #         operation=operation))

        await gather_with_concurrency(*operation_tasks)

    async def add_data_quality_violations(
            self,
            baseline_data_set: DriftDataSet,
            data: sqlalchemy.engine.base.Engine) -> None:
        self.data_quality_violations = await DataQualityIssue.get_violations_count(data, data_set=self)

    def to_dict(self) -> dict:
        dict_ = super().to_dict()

        if self.record_id_column is not None:
            dict_["record_id_column"] = get_python_types(self.record_id_column)

        if self.record_timestamp_column is not None:
            dict_["record_timestamp_column"] = get_python_types(self.record_timestamp_column)

        if self.start_timestamp is not None:
            dict_["start_timestamp"] = self.start_timestamp.isoformat()

        if self.end_timestamp is not None:
            dict_["end_timestamp"] = self.end_timestamp.isoformat()

        if self.data_quality_violations is not None:
            dict_["data_quality_violations"] = get_python_types(self.data_quality_violations)

        return dict_
