# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2022
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

from time import time
from typing import Union

import numpy as np
import pandas as pd
import sqlalchemy
from ibm_metrics_plugin.clients.readers.async_query_executor import \
    execute_count_query
from ibm_metrics_plugin.common.utils.metrics_logger import MetricLogger
from ibm_metrics_plugin.metrics.drift_v2.entity.column.numerical_column import \
    NumericalColumn
from ibm_metrics_plugin.metrics.drift_v2.entity.data_quality.data_quality_issue import \
    DataQualityIssue
from ibm_metrics_plugin.metrics.drift_v2.entity.data_quality.rule.data_quality_rule import \
    DataQualityRule
from ibm_metrics_plugin.metrics.drift_v2.entity.dataset.data_set import \
    DriftDataSet
from ibm_metrics_plugin.metrics.drift_v2.entity.operation.operation import \
    Operation
from ibm_metrics_plugin.metrics.drift_v2.utils.constants import \
    DataQualityIssueKind
from ibm_metrics_plugin.metrics.drift_v2.utils.drift_utils import \
    get_logging_params

logger = MetricLogger(__name__)


class NumericalIQROutlier(DataQualityIssue):
    def __init__(self) -> None:
        super().__init__(DataQualityIssueKind.NUMERICAL_IQR_OUTLIER)

    async def learn(self,
                    target_column: NumericalColumn,
                    data_set: DriftDataSet,
                    operation: Operation,
                    data: Union[pd.DataFrame,
                                sqlalchemy.engine.base.Engine] = None) -> None:
        self.data_set_count = data_set.count

        lower_limit = target_column.percentiles[0.25] - 1.5 * target_column.iqr
        upper_limit = target_column.percentiles[0.75] + 1.5 * target_column.iqr

        self.summary = {
            "min": target_column.min_,
            "max": target_column.max_,
            "mean": target_column.mean,
            "std": target_column.std,
            "percentiles": target_column.percentiles,
            "iqr": target_column.iqr
        }

        self.rule = DataQualityRule(lower_limit=lower_limit, upper_limit=upper_limit)
        self.count = await self.get_count(
            lower_limit=lower_limit,
            upper_limit=upper_limit,
            target_column=target_column,
            data=data)

        if operation is not None:
            self.operation = operation.name
        self.target_column = target_column.name
        return self

    async def get_count(self,
                        lower_limit: float,
                        upper_limit: float,
                        target_column: NumericalColumn,
                        data: Union[pd.DataFrame,
                                    sqlalchemy.engine.base.Engine]) -> int:

        if isinstance(data, pd.DataFrame):
            lower_count = len(data[(data[target_column.name] < lower_limit)])
            upper_count = len(data[data[target_column.name] > upper_limit])
            return lower_count + upper_count

        query = target_column.outlier_query(lower_limit=lower_limit, upper_limit=upper_limit)
        count = await execute_count_query(query=query, data=data)
        return count

    def check_violations(self, transactions: pd.DataFrame, **kwargs) -> np.array:
        return ~transactions[self.target_column].between(
            left=self.rule.lower_limit, right=self.rule.upper_limit, inclusive="both")
