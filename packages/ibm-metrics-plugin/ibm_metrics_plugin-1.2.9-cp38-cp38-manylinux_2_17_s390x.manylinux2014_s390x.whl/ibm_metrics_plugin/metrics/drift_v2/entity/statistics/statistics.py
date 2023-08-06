# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2022
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

from abc import abstractclassmethod, abstractmethod
from uuid import uuid4

from ibm_metrics_plugin.metrics.drift_v2.entity.statistics.element import \
    Element
from ibm_metrics_plugin.metrics.drift_v2.utils.constants import MetricName


class Statistics:
    def __init__(self, target_column: str,
                 source_column: str = None,
                 source_value: str = None) -> None:
        self.id = str(uuid4())
        self.target_column = target_column
        self.elements = []
        self.kind = None
        self._name = None

        # properties
        self.drift_model_classification = None
        self.is_prediction_correct = None
        self.source_column = source_column
        self.source_value = source_value

    @property
    def name(self) -> str:
        if self._name != None:
            return self._name

        self._name = f"{self.kind.value}_{self.target_column}"

        if self.source_column:
            self._name += f"_{self.source_column}"
        if self.source_value:
            self._name += f"_{self.source_value}"
        return self._name

    @property
    def count(self) -> int:
        return int(sum(self.values))

    @property
    def fields(self) -> list:
        return [element.field for element in sorted(self.elements)]

    @property
    def values(self) -> list:
        return [element.value for element in sorted(self.elements)]

    def is_element_present(self, element: Element) -> bool:
        """Checks if the element is present in the statistics

        Args:
            element (DiscreteElement): The element to check

        Returns:
            bool: True if the element is present in the statistics, False otherwise
        """
        return element.field in self.fields

    def add_element(self, element: Element) -> None:
        if self.is_element_present(element):
            raise ValueError(f"Element {element.field} already exists in the statistics '{self.name}'")

        self.elements.append(element)

    def get_element_by_field(self, field: str) -> Element:
        for element in self.elements:
            if element.field == field:
                return element

        raise ValueError(f"Element {field} not found in the statistics '{self.name}'")

    def get_element_by_index(self, index: int) -> Element:
        return sorted(self.elements)[index]

    @abstractmethod
    def get_distance(
            self,
            other: "Statistics",
            metric_name: MetricName = None,
            return_local_intervals: bool = False,
            **kwargs) -> float:
        raise NotImplementedError

    @abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError

    @abstractclassmethod
    def from_dict(cls, data: dict) -> "Statistics":
        raise NotImplementedError
