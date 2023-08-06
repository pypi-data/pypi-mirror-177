# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2022
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

import json
from abc import abstractmethod
from time import time
from typing import Dict, List, Union

import pandas as pd
import sqlalchemy
from ibm_metrics_plugin.clients.readers.async_query_executor import \
    execute_query
from ibm_metrics_plugin.common.utils.metrics_logger import MetricLogger
from ibm_metrics_plugin.common.utils.python_utils import get_python_types
from ibm_metrics_plugin.metrics.drift_v2.entity.column.data_column import \
    DataColumn
from ibm_metrics_plugin.metrics.drift_v2.entity.data_quality.rule.data_quality_rule import \
    DataQualityRule
from ibm_metrics_plugin.metrics.drift_v2.entity.operation.operation import \
    Operation
from ibm_metrics_plugin.metrics.drift_v2.utils.async_utils import \
    gather_with_concurrency
from ibm_metrics_plugin.metrics.drift_v2.utils.constants import (
    DATA_QUALITY_ISSUES_COLUMN, DataQualityIssueKind)
from ibm_metrics_plugin.metrics.drift_v2.utils.drift_utils import \
    get_logging_params

logger = MetricLogger(__name__)


class DataQualityIssue:
    def __init__(self, kind: DataQualityIssueKind) -> None:
        self.kind = kind
        self.target_column = None
        self.operation = None
        self.count = 0
        self.data_set_count = 0
        self.summary = {}
        self.rule = None
        self._percent = None

    @property
    def name(self) -> str:
        """Returns the name of the data quality issue.

        Returns:
            str: The name of the data quality issue.
        """
        return f"{self.kind.value}_{self.target_column}"

    @property
    def file_name(self) -> str:
        """Returns the file name for the data quality issue.

        Returns:
            str: The file name for the data quality issue.
        """

        return f"{self.name}.json"

    @property
    def percent(self) -> float:
        if self.data_set_count == 0:
            return -1

        if self._percent is None:
            self._percent = (self.count / self.data_set_count)

        return self._percent

    @abstractmethod
    async def learn(self, target_column: DataColumn, data_set, operation: Operation = None,
                    data: Union[pd.DataFrame, sqlalchemy.engine.base.Engine] = None) -> None:
        raise NotImplementedError

    @classmethod
    def factory(cls,
                issue_kind: DataQualityIssueKind) -> "DataQualityIssue":
        if issue_kind is DataQualityIssueKind.MISSING_VALUE:
            from ibm_metrics_plugin.metrics.drift_v2.entity.data_quality.missing_value import \
                MissingValue

            return MissingValue()

        if issue_kind is DataQualityIssueKind.EMPTY_STRING:
            from ibm_metrics_plugin.metrics.drift_v2.entity.data_quality.empty_string import \
                EmptyString
            return EmptyString()

        if issue_kind is DataQualityIssueKind.CATEGORICAL_OUTLIER:
            from ibm_metrics_plugin.metrics.drift_v2.entity.data_quality.categorical_outlier import \
                CategoricalOutlier
            return CategoricalOutlier()

        if issue_kind is DataQualityIssueKind.NUMERICAL_IQR_OUTLIER:
            from ibm_metrics_plugin.metrics.drift_v2.entity.data_quality.numerical_iqr_outlier import \
                NumericalIQROutlier
            return NumericalIQROutlier()

    @classmethod
    def score(cls, transactions: pd.DataFrame,
              baseline_data_set,
              record_id_column: str = "scoring_id",
              record_timestamp_column: str = "scoring_timestamp") -> List:

        result_dict = {(issue.kind.value, issue.target_column): issue.check_violations(
            transactions) for issue in baseline_data_set.data_quality_issues.values()}
        result = pd.DataFrame(result_dict, index=transactions.index)

        def apply_fn(row):
            import json
            filtered_issues = row.index.values[row.values]
            result = {}
            _ = [result.setdefault(issue, []).append(column) for (issue, column) in filtered_issues]
            return json.dumps(result)

        result = result.apply(apply_fn, axis=1)
        return result

    @abstractmethod
    def check_violations(self, transactions: pd.DataFrame, **kwargs):
        raise NotImplementedError

    @classmethod
    async def get_violations_count(cls, data: sqlalchemy.engine.base.Engine,
                                   data_set) -> Dict[str, Dict[str, int]]:
        violations_count = {}

        if "ibm" in data_set.dialect:
            violations_count = await cls.get_violations_count_db2(data, data_set)

        elif "postgres" in data_set.dialect:
            violations_count = await cls.get_violations_count_postgres(data, data_set)

        return violations_count

    @classmethod
    def get_violations_count_db2(cls, data: sqlalchemy.engine.base.Engine,
                                 data_set) -> Dict[str, Dict[str, int]]:
        violations_count = {}
        with data.connect().execution_options(stream_results=True) as conn:
            query = f"select \"{DATA_QUALITY_ISSUES_COLUMN}\""
            query += f" WHERE \"{DATA_QUALITY_ISSUES_COLUMN}\" !=" + " '{}'"
            query += f" from {data_set.full_table_name}"

            def aggregate(row):
                row = json.loads(row)
                for issue, column_list in row.items():
                    if issue not in violations_count:
                        violations_count[issue] = {col: 1 for col in column_list}
                    else:
                        violations_count[issue].update(
                            {col: (violations_count[issue][col] + 1 if col in violations_count[issue] else 1) for col in column_list})

            for chunk in pd.read_sql(query, conn, chunksize=1000):
                _ = chunk.squeeze().apply(aggregate)
        return violations_count

    @classmethod
    async def get_violations_count_postgres(
            cls, data: sqlalchemy.engine.base.Engine, data_set) -> Dict[str, Dict[str, int]]:

        start_time = time()
        violations_count = {}

        issue_tasks = []
        for issue_kind in DataQualityIssueKind:
            query = "select violations, count(violations) as count"
            query += f" from {data_set.full_table_name},"
            query += f" jsonb_array_elements_text(\"{DATA_QUALITY_ISSUES_COLUMN}\"->'{issue_kind.value}') as violations"
            query += f" group by 1 order by 1;"

            issue_tasks.append(execute_query(query=query, data=data))

        result = await gather_with_concurrency(*issue_tasks)

        for issue_kind, counts in zip(DataQualityIssueKind, result):
            counts.set_index("violations", inplace=True)
            violations_count[issue_kind.value] = counts.squeeze().to_dict()

        logger.log_info(
            "Computed the violations count",
            get_logging_params(
                data_set=data_set,
                start_time=start_time))
        return violations_count

    def to_dict(self) -> Dict:
        dict_ = {
            "name": self.name,
            "kind": self.kind.value,
            "target_column": self.target_column,
            "operation": self.operation,
            "rule": self.rule.to_dict(),
            "data_quality_issues": get_python_types(self.count),
            "data_set_count": get_python_types(self.data_set_count),
            "data_quality_score": get_python_types(self.percent)
        }

        if self.summary:
            dict_["summary"] = get_python_types(self.summary)

        return dict_

    def to_summary_dict(self) -> dict:
        """Converts the data quality issue to a dictionary to be included in summary.json

        Returns:
            dict: The data quality issue as a dictionary
        """
        dict_ = {
            "name": self.name,
            "kind": self.kind.value,
            "target_column": self.target_column,
            "file_name": self.file_name
        }
        return dict_

    @classmethod
    def from_dict(self, dict_: Dict) -> "DataQualityIssue":
        from ibm_metrics_plugin.metrics.drift_v2.entity.data_quality.categorical_outlier import \
            CategoricalOutlier
        from ibm_metrics_plugin.metrics.drift_v2.entity.data_quality.empty_string import \
            EmptyString
        from ibm_metrics_plugin.metrics.drift_v2.entity.data_quality.missing_value import \
            MissingValue
        from ibm_metrics_plugin.metrics.drift_v2.entity.data_quality.numerical_iqr_outlier import \
            NumericalIQROutlier

        try:
            if dict_["kind"] == DataQualityIssueKind.MISSING_VALUE.value:
                dq = MissingValue()
            elif dict_["kind"] == DataQualityIssueKind.CATEGORICAL_OUTLIER.value:
                dq = CategoricalOutlier()
            elif dict_["kind"] == DataQualityIssueKind.EMPTY_STRING.value:
                dq = EmptyString()
            elif dict_["kind"] == DataQualityIssueKind.NUMERICAL_IQR_OUTLIER.value:
                dq = NumericalIQROutlier()

            dq.target_column = dict_["target_column"]
            dq.operation = dict_["operation"]
            dq.count = dict_["data_quality_issues"]
            dq.data_set_count = dict_["data_set_count"]
            dq.rule = DataQualityRule.from_dict(dict_["rule"])
            return dq

        except KeyError as e:
            raise ValueError(
                f"Cannot create a data quality issue from the given dictionary. Missing key {e}.") from e
