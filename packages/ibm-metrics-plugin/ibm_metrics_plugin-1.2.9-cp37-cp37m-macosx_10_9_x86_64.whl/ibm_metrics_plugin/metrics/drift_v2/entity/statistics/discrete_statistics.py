# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2022
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

from time import time
from typing import List, Union

import numpy as np
from ibm_metrics_plugin.common.utils.metrics_logger import MetricLogger
from ibm_metrics_plugin.common.utils.python_utils import get, get_python_types
from ibm_metrics_plugin.metrics.drift_v2.entity.statistics.element import \
    DiscreteElement
from ibm_metrics_plugin.metrics.drift_v2.entity.statistics.interval import \
    Interval
from ibm_metrics_plugin.metrics.drift_v2.entity.statistics.statistics import \
    Statistics
from ibm_metrics_plugin.metrics.drift_v2.utils.constants import (
    RANDOM_SEED, DiscreteMetricName, MetricName, StatisticsKind)
from ibm_metrics_plugin.metrics.drift_v2.utils.control_box import \
    ControlBoxManager
from ibm_metrics_plugin.metrics.drift_v2.utils.drift_utils import \
    get_logging_params

logger = MetricLogger(__name__)


class DiscreteStatistics(Statistics):
    def __init__(self, target_column: str,
                 source_column: str = None,
                 source_value: str = None) -> None:
        super().__init__(target_column, source_column, source_value)
        self.has_statistical_buffers = False
        self.kind = StatisticsKind.DISCRETE

    @property
    def distinct_count(self) -> int:
        return len(self.fields)

    @property
    def min_(self) -> Union[str, int, float]:
        return sorted(self.elements)[0].field

    @property
    def max_(self) -> Union[str, int, float]:
        return sorted(self.elements)[-1].field

    @property
    def normalized_values(self) -> np.array:
        """The normalized values of the statistics

        Returns:
            np.array: The normalized values of the statistics
        """

        if all(x == 0 for x in self.values):
            return np.zeros(len(self.values))

        normalized_values_ = [element.normalized_value for element in sorted(self.elements)]

        if any((value < 0 or value > 1) for value in normalized_values_):
            for element in self.elements:
                element.normalized_value = element.value / np.sum(self.values)
            normalized_values_ = [element.normalized_value for element in sorted(self.elements)]

        if sum(normalized_values_) != 1:
            for element in self.elements:
                element.normalized_value = element.value / np.sum(self.values)
            normalized_values_ = [element.normalized_value for element in sorted(self.elements)]

        return np.array(normalized_values_)

    def fix_missing(self, other: "DiscreteStatistics") -> None:
        """Checks the values that are present in the other statistics
        and missing in the current statistics. If the value is missing,
        it's value is set to 0.

        Args:
            other (DiscreteStatistics): The other statistics to check
        """
        start_time = time()
        original_count = len(self.fields)
        for label in other.fields:
            if label not in self.fields:
                self.add_element(DiscreteElement(label, 0))

        new_count = len(self.fields)
        logger.log_debug(
            f"Added {new_count - original_count} missing elements.",
            get_logging_params(
                start_time=start_time,
                statistics=self))

    def update_zero_elements(self):
        """Updates the elements with zero values to have a value of 1
        """

        for element in self.elements:
            if element.value == 0:
                element.value = 1
                element.normalized_value = -1

    def get_distance(self, other: "Statistics", metric_name: MetricName = None,
                     return_local_intervals: bool = False, **kwargs) -> Union[float, List[Interval]]:
        """Computes the distance between the current statistics and the other statistics.
        The only metric currently supported is the Jensen-Shannon distance. This also returns
        the categories with statistics changes, if return_local_intervals is True.

        Args:
            other (Statistics): The other statistics to compare with
            metric_name (MetricName, optional): The metric name. Defaults to None. If None, the Jensen-Shannon distance is used.
            return_local_intervals (bool, optional): Also, return the categories with change percentages if set to True. Defaults to False.

        Raises:
            ValueError: If the metric name is not supported

        Returns:
            Union[float, List[Interval]]: Returns two things:
            1. distance(float): The distance between the statistics
            2. categories(List[Interval]): The local intervals if return_local_intervals is True
        """
        start_time = time()
        if metric_name is None:
            metric_name = DiscreteMetricName.JENSEN_SHANNON

        if metric_name != DiscreteMetricName.JENSEN_SHANNON:
            raise ValueError(f"Unsupported metric name: {metric_name}")

        self.fix_missing(other)
        other.fix_missing(self)

        from ibm_metrics_plugin.metrics.drift_v2.utils.statistics_utils import \
            get_jensen_shannon_distance
        distance, elementwise_contribution = get_jensen_shannon_distance(self, other)

        if return_local_intervals:
            from ibm_metrics_plugin.metrics.drift_v2.utils.statistics_utils import \
                get_significant_categories

            significant_categories = get_significant_categories(
                self, other, elementwise_contribution)
            logger.log_info(
                f"Computed {distance} distance using {metric_name} and {len(significant_categories)} local intervals.",
                get_logging_params(
                    start_time=start_time,
                    statistics=self))
            return distance, significant_categories

        logger.log_info(
            f"Computed {distance} distance using {metric_name}.",
            get_logging_params(
                start_time=start_time,
                statistics=self))
        return distance

    def compute_buffer(self):
        """Computes the statistical buffer for every value in the statistics

        Raises:
            ValueError: If all the values are 0 in the statistics
        """

        if all(x == 0 for x in self.values):
            raise ValueError("Cannot compute buffer for a statistics with all zeros")

        start_time = time()
        self.update_zero_elements()

        random_generator = np.random.default_rng(seed=RANDOM_SEED)
        sampled_frequencies = random_generator.multinomial(
            n=int(
                np.sum(
                    self.values)),
            pvals=self.normalized_values,
            size=ControlBoxManager().get_control_box().get_categorical_multinomial_samples())

        percent_change_sampled = np.abs((sampled_frequencies - self.values) / self.values)

        # With the default value of alpha = 0.05, the statistical buffer is the
        # 95th percentile of the percent change statistics.
        statistical_buffer = np.quantile(
            percent_change_sampled,
            axis=0,
            q=1 - ControlBoxManager().get_control_box().get_categorical_buffer_alpha())

        for i in range(len(self.fields)):
            self.get_element_by_index(i).statistical_buffer = statistical_buffer[i]

        self.has_statistical_buffers = True
        logger.log_info(
            f"Computed statistical buffer.",
            get_logging_params(
                start_time=start_time,
                statistics=self))

    def to_dict(self) -> dict:
        """Converts the statistics to a dictionary

        Returns:
            dict: The dictionary representation of the statistics.
        """
        dict_ = {
            "id": self.id,
            "kind": self.kind.value,
            "summary": {
                "count": get_python_types(self.count),
                "distinct_count": get_python_types(self.distinct_count),
                "min": get_python_types(self.min_),
                "max": get_python_types(self.max_)
            },
            "frequency_counts": {
                "fields": get_python_types(self.fields),
                "values": get_python_types(self.values)
            },
            "percentages/densities": {
                "fields": get_python_types(self.fields),
                "values": get_python_types(self.normalized_values)
            },
            "target_column": self.target_column
        }

        if self.has_statistical_buffers:
            dict_["statistical_buffers"] = {
                "fields": get_python_types(
                    self.fields), "values": [
                    get_python_types(
                        element.statistical_buffer) for element in sorted(
                        self.elements)]}

        if self.is_prediction_correct is not None:
            dict_["is_prediction_correct"] = self.is_prediction_correct

        if self.drift_model_classification is not None:
            dict_["drift_model_classification"] = self.drift_model_classification

        if self.source_column is not None:
            dict_["source_column"] = self.source_column

        if self.source_value is not None:
            dict_["source_value"] = get_python_types(self.source_value)

        return dict_

    @classmethod
    def from_dict(cls, data: dict) -> "DiscreteStatistics":
        """Converts a dictionary to a statistics

        Args:
            data (dict): The dictionary to convert

        Raises:
            ValueError: If the data is not a valid statistics

        Returns:
            DiscreteStatistics: The statistics
        """
        try:
            frequency_counts = data["frequency_counts"]
            statistics = cls(target_column=data["target_column"],
                               source_column=get(data, "source_column"),
                               source_value=get(data, "source_value"))
            statistics.id = data["id"]
            statistics.kind = StatisticsKind(data["kind"])

            for field, value in zip(frequency_counts["fields"], frequency_counts["values"]):
                statistics.add_element(DiscreteElement(field, value))

            _ = statistics.normalized_values

            if "statistical_buffers" in data:
                statistics.has_statistical_buffers = True
                statistical_buffers = data["statistical_buffers"]
                for field, value in zip(
                        statistical_buffers["fields"], statistical_buffers["values"]):
                    statistics.get_element_by_field(field).statistical_buffer = value

            statistics.is_prediction_correct = get(data, "is_prediction_correct")
            statistics.drift_model_classification = get(data, "drift_model_classification")

            return statistics
        except KeyError as e:
            raise ValueError(
                f"Cannot create DiscreteStatistics from the given dictionary. Missing key: {e}") from e
