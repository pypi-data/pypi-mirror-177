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


class DataQualityRule:
    """
    Rules
        - [] Array of feature_values Rule
        - [] RegEx Rule
        - [] Limits Rule
    """

    def __init__(self, **kwargs) -> None:
        self.lower_limit = None
        self.upper_limit = None
        self.feature_values = None
        self.regex_str = None
        self._description = None
        if "regex_str" in kwargs:
            self.regex_str = kwargs["regex_str"]
        elif "feature_values" in kwargs:
            self.feature_values = kwargs["feature_values"]
        else:
            if "lower_limit" in kwargs:
                self.lower_limit = kwargs["lower_limit"]

            if "upper_limit" in kwargs:
                self.upper_limit = kwargs["upper_limit"]

    def get_description(self) -> str:
        if self._description is not None:
            return self._description

        if self.regex_str is not None:
            self._description = f"Any value that matches the regular expression '{self.regex_str}' in the data."
            return self._description

        if self.feature_values is not None:
            self._description = f"Any value that is not included in 'feature_values' in the data."
            return self._description

        limit_strs = []
        if self.lower_limit is not None:
            limit_strs.append(f"< {self.lower_limit}")

        if self.upper_limit is not None:
            limit_strs.append(f"> {self.upper_limit}")

        limit_strs = " or ".join(limit_strs)
        self._description = f"Any value which is {limit_strs} in the data."
        return self._description

    def to_dict(self) -> Dict:
        if (self.regex_str is None) and (self.feature_values is None) and (
                self.lower_limit is None) and (self.upper_limit is None):
            raise ValueError(
                "None of 'regex_str', 'feature_values', 'lower_limit' and 'upper_limit' are set.")

        dict_ = {}

        if self.regex_str is not None:
            dict_["regex"] = get_python_types(self.regex_str)
        elif self.feature_values is not None:
            dict_["feature_values"] = get_python_types(self.feature_values)
        else:
            if self.lower_limit is not None:
                dict_["lower_limit"] = get_python_types(self.lower_limit)
            if self.upper_limit is not None:
                dict_["upper_limit"] = get_python_types(self.upper_limit)

        dict_["description"] = self.get_description()
        return dict_

    @classmethod
    def from_dict(cls, dict_: Dict) -> "DataQualityRule":
        rule = cls()
        if "regex_str" in dict_:
            rule.regex_str = dict_["regex_str"]
        elif "feature_values" in dict_:
            rule.feature_values = dict_["feature_values"]
        else:
            if "lower_limit" in dict_:
                rule.lower_limit = dict_["lower_limit"]

            if "upper_limit" in dict_:
                rule.upper_limit = dict_["upper_limit"]

        return rule
