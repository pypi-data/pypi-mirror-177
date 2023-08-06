# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2022
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

from time import time
from typing import List

from ibm_metrics_plugin.common.utils.metrics_logger import MetricLogger
from ibm_metrics_plugin.metrics.drift_v2.entity.column.data_column import \
    DataColumn
from ibm_metrics_plugin.metrics.drift_v2.entity.dataset.data_set import \
    DriftDataSet
from ibm_metrics_plugin.metrics.drift_v2.entity.insight.insight import Insight
from ibm_metrics_plugin.metrics.drift_v2.entity.statistics.interval import \
    Interval
from ibm_metrics_plugin.metrics.drift_v2.entity.statistics.statistics import \
    Statistics
from ibm_metrics_plugin.metrics.drift_v2.utils.constants import (
    META_MODEL_CLASSIFICATION_COLUMN, META_MODEL_TARGET_COLUMN,
    PredictionClassification)
from ibm_metrics_plugin.metrics.drift_v2.utils.drift_utils import \
    get_logging_params

logger = MetricLogger(__name__)


class AccuracyInsight(Insight):
    def __init__(self) -> None:
        super().__init__()
        self.compare_full_column = False  # TODO find better name please

    @property
    def name(self):
        if self.compare_full_column:
            return f"accuracy_insights_{self.source_column}_{self.source_value}_{self.target_column}"

        return f"accuracy_insights_{self.source_column}_{self.source_value}_{self.target_column}_incorrect"

    @classmethod
    def compute_with_full_baseline(
            cls,
            baseline_data_set: DriftDataSet,
            statistics: Statistics) -> "AccuracyInsight":
        start_time = time()

        baseline_column = baseline_data_set.get_column(column_name=META_MODEL_TARGET_COLUMN)
        target_column = baseline_data_set.get_column(statistics.target_column)
        baseline_statistics = baseline_data_set.get_statistics(target_column=target_column)
        if baseline_statistics is None:
            logger.log_info(
                f"No baseline statistics found for {target_column.name}",
                get_logging_params(
                    statistics=statistics))
            return

        score = baseline_statistics.get_distance(statistics)
        if score == 0:
            return

        insight = AccuracyInsight()
        insight.compare_full_column = True
        insight.insight_score = score
        insight.source_column = baseline_column.name
        insight.source_value = PredictionClassification.INCORRECT.value
        insight.target_column = statistics.target_column
        insight.baseline_statistics = baseline_statistics
        insight.production_statistics = statistics
        logger.log_debug(
            "Insight added",
            get_logging_params(
                insight=insight,
                start_time=start_time))

        return insight

    @classmethod
    def compute_with_incorrect_baseline(cls,
                                        baseline_data_set: DriftDataSet,
                                        statistics: Statistics) -> "AccuracyInsight":
        start_time = time()

        baseline_column = baseline_data_set.get_column(column_name=META_MODEL_TARGET_COLUMN)
        target_column = baseline_data_set.get_column(statistics.target_column)
        baseline_statistics = baseline_data_set.get_statistics(
            source_column=baseline_column,
            source_value=PredictionClassification.INCORRECT.value,
            target_column=target_column)
        if baseline_statistics is None:
            logger.log_info(
                f"No baseline statistics found for {baseline_column.name}={PredictionClassification.INCORRECT.value}",
                get_logging_params(
                    statistics=statistics))
            return

        score = baseline_statistics.get_distance(statistics)
        if score == 0:
            return

        insight = AccuracyInsight()
        insight.insight_score = 1 - score  # TODO add reason
        insight.source_column = baseline_column.name
        insight.source_value = PredictionClassification.INCORRECT.value
        insight.target_column = statistics.target_column
        insight.baseline_statistics = baseline_statistics
        insight.production_statistics = statistics
        logger.log_debug(
            "Insight added",
            get_logging_params(
                insight=insight,
                start_time=start_time))

        return insight

    @classmethod
    def compute(
            cls,
            baseline_data_set: DriftDataSet,
            production_data_set: DriftDataSet,
            interval: Interval = None,
            column: DataColumn = None) -> List["AccuracyInsight"]:

        start_time = time()
        insights = []

        production_column = production_data_set.get_column(
            column_name=META_MODEL_CLASSIFICATION_COLUMN)
        source_value = PredictionClassification.INCORRECT.value
        production_statistics = production_data_set.get_all_statistics(
            column=production_column, value=source_value)

        # Compute insights for incorrect predictions in production with incorrect
        # predictions in baseline

        for _, statistics in production_statistics.items():
            print(statistics.name)
            insight = cls.compute_with_incorrect_baseline(
                baseline_data_set=baseline_data_set, statistics=statistics)

            if insight is not None:
                insights.append(insight)

            insight = cls.compute_with_full_baseline(
                baseline_data_set=baseline_data_set, statistics=statistics)

            if insight is not None:
                insights.append(insight)

        logger.log_info(
            f"{len(insights)} added",
            get_logging_params(
                column=column,
                data_set=production_data_set,
                start_time=start_time))

        # Compute insights for incorrect predictions in production with full column in baseline data
        return insights
