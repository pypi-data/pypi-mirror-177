# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2022
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

from functools import total_ordering
from typing import Union

import numpy as np
from ibm_metrics_plugin.common.utils.python_utils import get_python_types
from ibm_metrics_plugin.metrics.drift_v2.utils.constants import (INFINITY,
                                                                 DataSetType)
from ibm_metrics_plugin.metrics.drift_v2.utils.control_box import \
    ControlBoxManager


@total_ordering
class Interval:
    def __init__(self, field: Union[str, int, float]) -> None:
        self.field = field
        self.values = []
        self._absolute_change_percentage = -1
        self._eligible_for_insights = None
        self.insights_available = False

    @property
    def absolute_change_percentage(self) -> float:
        if self._absolute_change_percentage == -1:
            self._absolute_change_percentage = self._calculate_absolute_change_percentage()
        return self._absolute_change_percentage

    @property
    def eligible_for_insights(self) -> bool:
        if self._eligible_for_insights is not None:
            return self._eligible_for_insights

        threshold = ControlBoxManager().get_control_box().get_interval_count_insights_threshold()
        # Calculate insights only if either of  baseline/production percentages > threshold.
        self._eligible_for_insights = (
            self.values[0].percentage >= threshold) or (
            self.values[1].percentage >= threshold)
        return self._eligible_for_insights

    def _calculate_absolute_change_percentage(self) -> float:
        if len(self.values) != 2:
            return -1

        baseline_value = next(
            value for value in self.values if value.type == DataSetType.BASELINE)
        production_value = next(
            value for value in self.values if value.type == DataSetType.PRODUCTION)

        if (baseline_value is None) or (production_value is None):
            return -1

        if baseline_value.absolute_count == 0:
            return np.inf

        return np.abs(
            (production_value.percentage -
             baseline_value.percentage) /
            baseline_value.percentage)

    def add_baseline_value(self, absolute_count: int, percentage: float) -> None:
        self.values.append(IntervalValue(DataSetType.BASELINE, absolute_count, percentage))

    def add_production_value(self, absolute_count: int, percentage: float) -> None:
        self.values.append(IntervalValue(
            DataSetType.PRODUCTION, absolute_count, percentage))

    def get_baseline_value(self) -> "IntervalValue":
        return next(value for value in self.values if value.type == DataSetType.BASELINE)

    def get_production_value(self) -> "IntervalValue":
        return next(value for value in self.values if value.type == DataSetType.PRODUCTION)

    def __lt__(self, other) -> bool:
        raise NotImplementedError

    def __eq__(self, other) -> bool:
        raise NotImplementedError

    def to_dict(self) -> dict:
        raise NotImplementedError

    @classmethod
    def from_dict(cls, dict_: dict) -> "Interval":
        raise NotImplementedError


class ContinuousStatisticsInterval(Interval):
    def __init__(self, lower_bound: Union[int, float], upper_bound: Union[int, float]) -> None:
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        super().__init__(f"{lower_bound}-{upper_bound}")

    def __lt__(self, other) -> bool:
        if self.absolute_change_percentage == other.absolute_change_percentage:
            if self.lower_bound == other.lower_bound:
                return self.upper_bound < other.upper_bound
            return self.lower_bound < other.lower_bound

        return self.absolute_change_percentage < other.absolute_change_percentage

    def __eq__(self, other) -> bool:
        return self.absolute_change_percentage == other.absolute_change_percentage and \
            self.lower_bound == other.lower_bound and self.upper_bound == other.upper_bound

    def to_dict(self) -> dict:
        return {
            "id": get_python_types(self.id),
            "field": get_python_types(
                self.field),
            "lower_bound": get_python_types(
                self.lower_bound),
            "upper_bound": get_python_types(
                self.upper_bound),
            "absolute_change_percentage": get_python_types(
                self.absolute_change_percentage) if self.absolute_change_percentage != np.inf else INFINITY,
            "eligible_for_insights": get_python_types(
                self.eligible_for_insights),
            "insights_available": get_python_types(
                self.insights_available),
            "values": [
                value.to_dict() for value in self.values]}

    @classmethod
    def from_dict(cls, dict_: dict) -> "ContinuousStatisticsInterval":
        try:
            interval = ContinuousStatisticsInterval(
                dict_["lower_bound"], dict_["upper_bound"])

            for value in dict_["values"]:
                interval.add_value(IntervalValue.from_dict(value))

            _ = interval.absolute_change_percentage

            interval.eligible_for_insights = dict_["eligible_for_insights"]
            interval.insights_available = dict_["insights_available"]
            return interval
        except KeyError as e:
            raise ValueError(f"Missing key {e} in dict {dict_}") from e


class DiscreteStatisticsInterval(Interval):
    def __init__(self, field: Union[str, int, float]) -> None:
        super().__init__(field)
        self.contribution_to_distance = -1
        self.statistical_buffer = -1

    @property
    def is_change_significant(self) -> bool:
        return self.absolute_change_percentage and (
            self.absolute_change_percentage > self.statistical_buffer)

    def __lt__(self, other) -> bool:
        if self.absolute_change_percentage == other.absolute_change_percentage:
            return self.contribution_to_distance < other.contribution_to_distance
        return self.absolute_change_percentage < other.absolute_change_percentage

    def __eq__(self, other) -> bool:
        return (self.absolute_change_percentage == other.absolute_change_percentage) \
            and (self.contribution_to_distance == other.contribution_to_distance)

    def to_dict(self) -> dict:
        return {
            "id": get_python_types(self.id),
            "field": get_python_types(
                self.field),
            "contribution_to_distance": get_python_types(
                self.contribution_to_distance),
            "absolute_change_percentage": get_python_types(
                self.absolute_change_percentage) if self.absolute_change_percentage != np.inf else INFINITY,
            "is_change_significant": get_python_types(
                self.is_change_significant),
            "statistical_buffer": get_python_types(
                self.statistical_buffer),
            "eligible_for_insights": get_python_types(
                self.eligible_for_insights),
            "insights_available": get_python_types(
                self.insights_available),
            "values": [
                value.to_dict() for value in self.values]}

    @classmethod
    def from_dict(cls, dict_: dict) -> "DiscreteStatisticsInterval":
        try:
            interval = DiscreteStatisticsInterval(dict_["field"])

            interval.contribution_to_distance = dict_[
                "contribution_to_distance"]
            interval.statistical_buffer = dict_["statistical_buffer"]
            _ = interval.absolute_change_percentage
            interval.eligible_for_insights = dict_["eligible_for_insights"]
            interval.insights_available = dict_["insights_available"]

            for value in dict_["values"]:
                interval.add_value(IntervalValue.from_dict(value))
        except KeyError as e:
            raise ValueError(f"Invalid interval dict: {dict_}") from e


class IntervalValue:
    def __init__(self, type: DataSetType, absolute_count: int, percentage: float) -> None:
        self.type = type
        self.absolute_count = absolute_count
        self.percentage = percentage

    def to_dict(self) -> dict:
        return {
            "type": get_python_types(self.type.value),
            "absolute_count": get_python_types(int(self.absolute_count)),
            "percentage": get_python_types(self.percentage)
        }

    @classmethod
    def from_dict(cls, interval_value: dict) -> "IntervalValue":
        try:
            return IntervalValue(
                DataSetType(interval_value["type"]),
                interval_value["absolute_count"],
                interval_value["percentage"])
        except KeyError as e:
            raise ValueError(
                f"Invalid interval value dict: {interval_value}") from e
