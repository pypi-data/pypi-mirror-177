# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2022
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------


import re
from typing import Union

import numpy as np
import pandas as pd
import sqlalchemy
from ibm_metrics_plugin.metrics.drift_v2.entity.column.data_column import \
    DataColumn
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


class EmptyString(DataQualityIssue):
    REGEX_STR = "\\A\\s*\\Z"

    def __init__(self) -> None:
        super().__init__(DataQualityIssueKind.EMPTY_STRING)

    async def learn(self, target_column: DataColumn, data_set: DriftDataSet, operation: Operation = None,
                    data: Union[pd.DataFrame, sqlalchemy.engine.base.Engine] = None) -> None:

        if operation is None:
            raise ValueError(f"No operation has been supplied.")

        self.data_set_count = data_set.count
        statistics = list(operation.statistics.values())[0]
        regex_str = re.compile(EmptyString.REGEX_STR)

        self.rule = DataQualityRule(regex_str=EmptyString.REGEX_STR)

        fields = []
        values = []

        for field, value in zip(statistics.fields, statistics.values):
            if regex_str.fullmatch(str(field)):
                fields.append(field)
                values.append(value)

        self.summary = {
            "fields": fields,
            "values": values
        }

        self.count = sum(values)
        self.operation = operation.name
        self.target_column = operation.target_column.name
        return self

    def check_violations(self, transactions: pd.DataFrame, **kwargs) -> np.array:
        return transactions[self.target_column].astype(str).str.contains(
            EmptyString.REGEX_STR, regex=True).fillna(False)
