# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2022
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

from typing import Union
from functools import total_ordering


@total_ordering
class Element:
    def __init__(self, field: Union[str, int, float], value: int) -> None:
        self.field = field
        self.value = value

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, value: int) -> None:
        if value < 0:
            raise ValueError(
                f"Value must be greater than or equal to 0, got {value} for field {self.field}")
        self._value = value

    def __eq__(self, other) -> bool:
        return self.field == other.field

    def __lt__(self, other) -> bool:
        return self.field < other.field

    def __add__(self, other):
        return self.value + (other.value if isinstance(other, Element) else other)

    def __radd__(self, other):
        if other == 0:
            return self.value
        else:
            return self.__add__(other)


class DiscreteElement(Element):
    def __init__(self, field: Union[str, int, float], value: int) -> None:
        super().__init__(field, value)
        self.normalized_value = -1
        self.statistical_buffer = -1


class ContinuousElement(Element):
    def __init__(self, field: Union[int, float], value: int) -> None:
        super().__init__(field, value)
