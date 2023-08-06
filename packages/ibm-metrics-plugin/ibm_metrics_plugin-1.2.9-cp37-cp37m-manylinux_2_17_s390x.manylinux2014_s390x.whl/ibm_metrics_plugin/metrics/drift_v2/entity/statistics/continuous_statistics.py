# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2022
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

from time import time
from typing import List, Tuple, Union

import numpy as np
from ibm_metrics_plugin.common.utils.metrics_logger import MetricLogger
from ibm_metrics_plugin.common.utils.python_utils import get, get_python_types
from ibm_metrics_plugin.metrics.drift_v2.entity.statistics.statistics import \
    Statistics
from ibm_metrics_plugin.metrics.drift_v2.entity.statistics.element import \
    ContinuousElement
from ibm_metrics_plugin.metrics.drift_v2.entity.statistics.interval import \
    Interval
from ibm_metrics_plugin.metrics.drift_v2.utils.constants import (
    ContinuousMetricName, StatisticsKind, MetricName,
    SignificantIntervalMode)
from ibm_metrics_plugin.metrics.drift_v2.utils.control_box import \
    ControlBoxManager
from ibm_metrics_plugin.metrics.drift_v2.utils.drift_utils import \
    get_logging_params
from KDEpy import TreeKDE

logger = MetricLogger(__name__)


class ContinuousStatistics(Statistics):
    """

    Documenting the steps to compute the distance between two statistics.

    1. Find the combined minimum and maximum values
    2. Compute equidistant x_values between the combined minimum and maximum values. (10K by default)
    3. Compute the density values for each x_value for both statistics.
    4. Compute the distance between the two statistics using the above density values

    """

    def __init__(self, target_column: str,
                 bin_width: Union[int, float],
                 is_integer: bool,
                 source_column: str = None,
                 source_value: str = None) -> None:
        super().__init__(target_column, source_column, source_value)
        self.kde = None
        self.kind = StatisticsKind.CONTINUOUS
        self.min_ = None
        self.max_ = None
        self.mean = None
        self.bin_width = bin_width
        self.is_integer = is_integer

    def compute_summary(self) -> None:
        self.min_ = np.min(self.fields)

        if self.is_integer:
            self.bin_width = int(self.bin_width)

            if self.bin_width == 1:
                # Special case. There will be an extra bin due to this.
                self.max_ = np.max(self.fields) + self.bin_width
            else:
                self.max_ = np.max(self.fields) + self.bin_width - 1
        else:
            self.bin_width = round(self.bin_width, 8)
            self.max_ = np.max(self.fields) + 0.999 * self.bin_width
        self.mean = np.average(self.fields, weights=self.values)

    def get_combined_min(self, other: 'ContinuousStatistics') -> Union[float, int]:
        """Gets the combined minimum value of this statistics and the other statistics.

        Args:
            other (ContinuousStatistics): The other statistics.

        Returns:
            Union[float, int]: The combined minimum value.
        """

        return min(self.min_, other.min_)

    def get_combined_max(self, other: 'ContinuousStatistics') -> Union[float, int]:
        """Gets the combined maximum value of this statistics and the other statistics.

        Args:
            other (ContinuousStatistics): The other statistics.

        Returns:
            Union[float, int]: The combined maximum value.
        """
        return max(self.max_, other.max_)

    def fix_missing(self, other: 'ContinuousStatistics') -> None:
        """Fixes the missing values in this statistics to be the same as the other statistics.
        Check @_fix_missing for more details.

        Args:
            other (ContinuousStatistics): The other statistics.
        """

        combined_min = self.get_combined_min(other)
        combined_max = self.get_combined_max(other)

        return self._fix_missing(combined_min, combined_max)

    def _fix_missing(self, min_value: Union[float, int] = None,
                     max_value: Union[float, int] = None) -> None:
        """Fixes the missing values in this statistics between the minimum and maximum values such that..
        The new statistics bins contain both minimum and maximum values.

        Args:
            min_value (Union[float, int], optional): The minimum value. Defaults to None.
            max_value (Union[float, int], optional): The maximum value. Defaults to None.
        """

        start_time = time()
        original_count = len(self.fields)
        if min_value is None:
            min_value = self.min_

        if max_value is None:
            max_value = self.max_

        bins_to_the_left = 0
        bins_to_the_right = 0

        if min_value < self.min_:
            bins_to_the_left = np.ceil(
                (self.min_ - min_value) / self.bin_width).astype(int)
            min_value = self.min_ - bins_to_the_left * self.bin_width

        if max_value > self.max_:
            bins_to_the_right = np.ceil(
                (max_value - self.max_) / self.bin_width).astype(int)
            max_value = self.max_ + bins_to_the_right * self.bin_width

        non_zero_indices = np.floor(
            (np.array(
                self.fields) -
                min_value) /
            self.bin_width).astype(int)
        new_fields = np.arange(
            min_value,
            max_value,
            self.bin_width,
            dtype=(
                int if self.is_integer else None))
        new_values = np.zeros(new_fields.shape)
        new_values[non_zero_indices] = self.values

        self.elements = [
            ContinuousElement(
                field, value) for field, value in zip(
                new_fields, new_values)]
        new_count = len(self.fields)
        logger.log_info(
            f"Added {new_count - original_count} values to statistics",
            get_logging_params(
                start_time=start_time,
                statistics=self))

    def compute_density_values(self, x_values: list) -> List[float]:
        """Computes the density values for the given x_values.

        Args:
            x_values (list): The x_values for which the density values are to be computed.

        Raises:
            ValueError: If all values in the statistics are zeros.

        Returns:
            List[float]: The density values for the given x_values.
        """

        if all(value == 0 for value in self.values):
            raise ValueError(
                "Cannot compute density values for a statistics with all 0 values")

        # Categorise each x_value into a bin.
        bin_index = np.searchsorted(self.fields, x_values, side="right")

        # Reduce the bin_index by one to get the index of the left edge of the bin.
        bin_index = bin_index - 1

        # Get how many x_values are in each bin
        x_value_bin_counts = np.bincount(bin_index)

        # Compute the weight/count to be given to each x_value
        x_value_weights = np.zeros(len(x_values))
        for i, _ in enumerate(x_values):
            x_value_weights[i] = self.values[bin_index[i]] / \
                x_value_bin_counts[bin_index[i]]

        start_time = time()
        self.kde = TreeKDE(bw="ISJ", kernel="epa")
        density_values = self.kde.fit(
            data=x_values, weights=x_value_weights).evaluate(x_values)
        logger.log_info(
            f"Computed {len(x_values)} density values.",
            get_logging_params(
                start_time=start_time,
                statistics=self))

        return density_values

    def get_distance(self, other: 'Statistics', metric_name: MetricName = None,
                     return_local_intervals: bool = False, **kwargs) -> Union[float, List[Interval]]:
        """Computes the distance between this statistics and the other statistics.

        The supported metrics are:
        1. Total Variation: The total variation distance between the statistics. (0 if the statistics are the same)
        2. Overlap Coefficient: The overlap coefficient between the statistics. (0 if the statistics are the same)

        This also returns the local intervals of the statistics where the changes are significant.

        Args:
            other (Statistics): The other statistics.
            metric_name (MetricName, optional): The metric name. Defaults to Overlap Coefficient.
            return_local_intervals (bool, optional): Option to return the intervals with significant difference. Defaults to False.

        Raises:
            ValueError: If the metric_name is not supported.

        Returns:
            Union[float, List[Interval]]: Returns two things:
            1. distance(float): The distance between the statistics
            2. categories(List[Interval]): The local intervals if return_local_intervals is True
        """

        start_time = time()
        if metric_name is None:
            metric_name = ContinuousMetricName.OVERLAP_COEFFICIENT

        self.fix_missing(other)
        other.fix_missing(self)

        if metric_name == ContinuousMetricName.OVERLAP_COEFFICIENT:
            from ibm_metrics_plugin.metrics.drift_v2.utils.statistics_utils import \
                get_overlap_coefficient

            distance, paired_density = get_overlap_coefficient(self, other)
        elif metric_name == ContinuousMetricName.TOTAL_VARIATION:
            from ibm_metrics_plugin.metrics.drift_v2.utils.statistics_utils import \
                get_total_variation

            distance, paired_density = get_total_variation(self, other)
        else:
            raise ValueError(f"Unsupported metric name: {metric_name}")

        if return_local_intervals:
            from ibm_metrics_plugin.metrics.drift_v2.utils.statistics_utils import \
                get_significant_intervals

            mode = get(kwargs, "mode", SignificantIntervalMode.BOTH)
            significant_intervals = get_significant_intervals(self, other, paired_density, mode)
            logger.log_info(
                f"Computed {distance} distance using {metric_name} and {len(significant_intervals)} local intervals in {mode} mode.",
                get_logging_params(
                    start_time=start_time,
                    statistics=self))
            return distance, significant_intervals

        logger.log_info(
            f"Computed {distance} distance using {metric_name}.",
            get_logging_params(
                start_time=start_time,
                statistics=self))
        return distance

    def get_count_for_range(self, bounds: Tuple) -> int:
        lower_bound = bounds[0]
        upper_bound = bounds[1]

        if (upper_bound - lower_bound) < self.bin_width:
            return 0
        # TODO Get the edge bin counts proportionately.

        elements = filter(lambda elem: (lower_bound <= elem.field <= upper_bound), self.elements)

        return sum(elem.value for elem in elements)

    def to_dict(self) -> dict:
        """Converts the statistics to a dictionary.

        Returns:
            dict: The dictionary representation of the statistics.
        """

        if (self.min_ is None) or (self.max_ is None):
            self.compute_summary()

        num_samples = ControlBoxManager().get_control_box().get_continuous_statistics_plot_samples() + 1
        density_x = np.linspace(self.min_, self.max_, num=num_samples)
        density_y = self.compute_density_values(density_x)

        dict_ = {
            "id": self.id,
            "kind": self.kind.value,
            "summary": {
                "count": get_python_types(self.count),
                "min": get_python_types(self.min_),
                "max": get_python_types(self.max_),
                "mean": get_python_types(self.mean),
                "bin_width": get_python_types(self.bin_width),
                "is_integer": get_python_types(self.is_integer)
            },
            "frequency_counts": {
                "fields": get_python_types(self.fields),
                "values": get_python_types(self.values)
            },
            "percentages/densities": {
                "fields": get_python_types(density_x),
                "values": get_python_types(density_y)
            },
            "target_column": self.target_column
        }

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
    def from_dict(cls, data: dict) -> 'ContinuousStatistics':
        """Converts the dictionary to a statistics.

        Args:
            data (dict): The dictionary representation of the statistics.

        Raises:
            ValueError: If the data is not a valid statistics.

        Returns:
            ContinuousStatistics: The statistics.
        """
        try:
            frequency_counts = data["frequency_counts"]
            statistics = cls(target_column=data["target_column"],
                               bin_width=data["summary"]["bin_width"],
                               is_integer=data["summary"]["is_integer"],
                               source_column=get(data, "source_column"),
                               source_value=get(data, "source_value"))
            statistics.id = data["id"]
            statistics.kind = StatisticsKind(data["kind"])

            for field, value in zip(frequency_counts["fields"], frequency_counts["values"]):
                statistics.add_element(ContinuousElement(field, value))

            statistics.compute_summary()
            statistics.is_prediction_correct = get(
                data, "is_prediction_correct")
            statistics.drift_model_classification = get(
                data, "drift_model_classification")

            return statistics
        except KeyError as e:
            raise ValueError(
                f"Cannot create ContinuousStatistics from the given dictionary. Missing key: {e}") from e
