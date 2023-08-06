# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2022
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

from typing import Dict

from ibm_metrics_plugin.common.utils.python_utils import get_python_types
from ibm_metrics_plugin.metrics.drift_v2.entity.column.data_column import \
    DataColumn
from ibm_metrics_plugin.metrics.drift_v2.utils.constants import (ColumnRole,
                                                                 ColumnType)


class CategoricalColumn(DataColumn):
    def __init__(self, name: str, role: ColumnRole) -> None:
        super().__init__(name, role)

        self.type = ColumnType.CATEGORICAL

    def to_dict(self) -> Dict:
        """Converts the object to a dictionary.

        Returns:
            Dict: The dictionary representation of the object.
        """        
        dict_ = {
            "type": self.type.value,
            "name": self.name,
            "role": self.role.value,
            "data_type": self.data_type,
            "feature_importance": get_python_types(self.feature_importance),
            "is_eligible_for_operation": self.is_eligible_for_operation,
            "is_eligible_for_data_quality": self.is_eligible_for_data_quality,
            "is_eligible_for_insights": self.is_eligible_for_insights
        }

        if self.distinct_count is not None:
            dict_["distinct_count"] = get_python_types(self.distinct_count)

        return dict_

    @classmethod
    def from_dict(cls, dict_: Dict) -> "CategoricalColumn":
        """Constructs a CategoricalColumn object from a dictionary.

        Args:
            dict_ (Dict): A dictionary containing the column information.

        Raises:
            ValueError: If there are any missing or invalid values in the dictionary.

        Returns:
            CategoricalColumn: A CategoricalColumn object.
        """
        try:
            column = cls(dict_["name"], ColumnRole(dict_["role"]))

            if "distinct_count" in dict_:
                column.distinct_count = dict_["distinct_count"]

            column.is_eligible_for_data_quality = dict_.get("is_eligible_for_data_quality", False)
            column.is_eligible_for_operation = dict_.get("is_eligible_for_operation", False)
            column.is_eligible_for_insights = dict_.get("is_eligible_for_insights", False)
            return column
        except KeyError as e:
            raise ValueError(
                f"Cannot create a data column from the given dictionary. Missing key {e}.") from e
