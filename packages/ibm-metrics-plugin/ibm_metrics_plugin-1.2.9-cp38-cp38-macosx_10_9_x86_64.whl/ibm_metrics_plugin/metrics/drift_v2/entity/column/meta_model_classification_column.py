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
from ibm_metrics_plugin.metrics.drift_v2.entity.column.categorical_column import \
    CategoricalColumn
from ibm_metrics_plugin.metrics.drift_v2.utils.async_utils import asyncify_fn
from ibm_metrics_plugin.metrics.drift_v2.utils.constants import (
    META_MODEL_CLASSIFICATION_COLUMN, META_MODEL_CONFIDENCE_COLUMN, ColumnRole,
    PredictionClassification)
from ibm_metrics_plugin.metrics.drift_v2.utils.control_box import \
    ControlBoxManager


class MetaModelClassificationColumn(CategoricalColumn):
    def __init__(self) -> None:
        super().__init__(META_MODEL_CLASSIFICATION_COLUMN, ColumnRole.META_MODEL_CLASSIFICATION)
        control_box = ControlBoxManager().get_control_box()
        self.lower_limit = control_box.get_meta_model_classification_lower_limit()
        self.upper_limit = control_box.get_meta_model_classification_upper_limit()

    async def count_distinct_rows(self, data: Union[pd.DataFrame, sqlalchemy.engine.base.Engine]) -> int:
        def fn(): return 3
        return await asyncify_fn(fn)

    def sub_query(self, other_column: str = None) -> str:
        sub_query = " (SELECT"

        if other_column is not None:
            sub_query += f" \"{other_column}\","

        sub_query += " CASE"
        sub_query += f" WHEN \"{META_MODEL_CONFIDENCE_COLUMN}\" >= {self.upper_limit} THEN '{PredictionClassification.INCORRECT.value}'"
        sub_query += f" WHEN \"{META_MODEL_CONFIDENCE_COLUMN}\" <= {self.lower_limit} THEN '{PredictionClassification.CORRECT.value}'"
        sub_query += f" ELSE '{PredictionClassification.UNSURE.value}'"
        sub_query += f" END as \"{self.name}\""
        sub_query += f" FROM {self.data_set.full_table_name}"
        sub_query += ") as sub_query"
        return sub_query
