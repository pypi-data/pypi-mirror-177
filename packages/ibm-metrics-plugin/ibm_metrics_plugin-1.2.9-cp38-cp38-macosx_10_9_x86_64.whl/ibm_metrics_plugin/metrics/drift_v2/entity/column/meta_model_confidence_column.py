# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2022
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

from typing import Union

import pandas as pd
import sqlalchemy
from ibm_metrics_plugin.metrics.drift_v2.entity.column.numerical_column import \
    NumericalColumn
from ibm_metrics_plugin.metrics.drift_v2.utils.constants import (
    META_MODEL_CONFIDENCE_COLUMN, ColumnRole)


class MetaModelConfidenceColumn(NumericalColumn):
    def __init__(self) -> None:
        super().__init__(META_MODEL_CONFIDENCE_COLUMN, ColumnRole.META_MODEL_PROBABILITY_SCORE)

        self.min_ = 0
        self.max_ = 1
        self.bin_width = 0.01
        self._is_discrete = False

    def compute_stats(self, data: Union[pd.DataFrame, sqlalchemy.engine.base.Engine]) -> None:
        return
