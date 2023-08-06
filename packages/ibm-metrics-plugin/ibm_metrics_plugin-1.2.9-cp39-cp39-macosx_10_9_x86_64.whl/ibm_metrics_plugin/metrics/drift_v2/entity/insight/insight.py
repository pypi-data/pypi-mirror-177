# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2022
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

from functools import total_ordering
from time import time
from typing import Dict, List

from ibm_metrics_plugin.common.utils.metrics_logger import MetricLogger
from ibm_metrics_plugin.common.utils.python_utils import get_python_types
from ibm_metrics_plugin.metrics.drift_v2.entity.column.data_column import \
    DataColumn
from ibm_metrics_plugin.metrics.drift_v2.entity.dataset.data_set import \
    DriftDataSet
from ibm_metrics_plugin.metrics.drift_v2.entity.statistics.continuous_statistics import \
    ContinuousStatistics
from ibm_metrics_plugin.metrics.drift_v2.entity.statistics.interval import (
    ContinuousStatisticsInterval, Interval)
from ibm_metrics_plugin.metrics.drift_v2.entity.operation.operation import \
    Operation
from ibm_metrics_plugin.metrics.drift_v2.utils.constants import DataSetType
from ibm_metrics_plugin.metrics.drift_v2.utils.drift_utils import \
    get_logging_params

logger = MetricLogger(__name__)


@total_ordering
class Insight:
    def __init__(self) -> None:
        self.source_column = None
        self.source_value = None
        self.insight_score = -1
        self.target_column = None
        self.baseline_statistics = None
        self.production_statistics = None

    @property
    def name(self):
        return f"insights_{self.source_column}_{self.source_value}_{self.target_column}"

    @property
    def file_name(self):
        return f"{self.name}.json"

    @classmethod
    def compute(self, baseline_data_set: DriftDataSet,
                production_data_set: DriftDataSet,
                interval: Interval,
                column: DataColumn,
                ) -> List["Insight"]:
        start_time = time()
        insights = []

        if isinstance(interval, ContinuousStatisticsInterval):
            value = (interval.lower_bound, interval.upper_bound)
        else:
            value = interval.field
        all_baseline_statistics = baseline_data_set.get_all_statistics(column=column, value=value)
        all_production_statistics = production_data_set.get_all_statistics(column=column, value=value)

        for name, statistics in all_production_statistics.items():
            insight_start_time = time()
            if name not in all_baseline_statistics:
                logger.log_info(
                    f"No baseline statistics found for {column.name}={value}",
                    get_logging_params(
                        statistics=statistics))
                continue

            baseline_statistics = all_baseline_statistics[name]

            score = baseline_statistics.get_distance(statistics)
            if score == 0:
                continue

            insight = Insight()
            insight.score = score
            insight.source_column = column.name
            insight.source_value = interval.field
            insight.target_column = statistics.target_column
            insight.baseline_statistics = baseline_statistics
            insight.production_statistics = statistics
            insights.append(insight)
            logger.log_debug(
                "Insight added",
                get_logging_params(
                    insight=insight,
                    start_time=insight_start_time))

        logger.log_info(
            f"{len(insights)} added",
            get_logging_params(
                column=column,
                data_set=production_data_set,
                start_time=start_time))
        return insights

    def __lt__(self, other) -> bool:
        return self.score < other.score

    def __eq__(self, other) -> bool:
        if other == None:
            return False
        return self.insight_score == other.insight_score

    def to_dict(self) -> Dict:
        baseline = self.baseline_statistics.to_dict()
        baseline["type"] = DataSetType.BASELINE.value
        production = self.production_statistics.to_dict()
        production["type"] = DataSetType.PRODUCTION.value

        return {
            "name": self.name,
            # "description": self.description,
            "score": get_python_types(self.score),
            "target_column": self.target_column,
            "source_column": self.source_column,
            "source_value": self.source_value,
            "statistics": [
                baseline,
                production
            ]
        }
