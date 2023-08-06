# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2022
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

from functools import total_ordering
from time import time
from typing import Dict, NamedTuple, Union

import pandas as pd
import sqlalchemy
from ibm_metrics_plugin.clients.readers.async_query_executor import \
    execute_count_query
from ibm_metrics_plugin.common.utils.constants import ProblemType
from ibm_metrics_plugin.common.utils.metrics_logger import MetricLogger
from ibm_metrics_plugin.metrics.drift_v2.utils.async_utils import asyncify_fn
from ibm_metrics_plugin.metrics.drift_v2.utils.constants import (ColumnRole,
                                                                 ColumnType)
from ibm_metrics_plugin.metrics.drift_v2.utils.control_box import \
    ControlBoxManager
from ibm_metrics_plugin.metrics.drift_v2.utils.drift_utils import \
    get_logging_params

logger = MetricLogger(__name__)


@total_ordering
class DataColumn:

    DataSetTuple = NamedTuple("data_set",
                              [("id", str),
                               ("count", int),
                               ("data_schema", dict),
                               ("problem_type", ProblemType),
                               ("feature_importance", dict),
                               ("dialect", str),
                               ("full_table_name", str)])

    def __init__(self, name: str, role: ColumnRole) -> None:
        self.name = name
        self.role = role
        self.distinct_count = None
        self.data_set = None
        self.type = ColumnType.GENERIC
        self._is_eligible_for_operation = None
        self._is_eligible_for_insights = None
        self._is_eligible_for_data_quality = None

    @property
    def count(self) -> int:
        """Gets the count of the column.

        Raises:
            ValueError: If the data set is not set.

        Returns:
            int: The count of the column.
        """

        if self.data_set is None:
            raise ValueError("DataSet is not set")
        return self.data_set.count

    @property
    def data_type(self) -> str:
        """Gets the data type of the column.

        Raises:
            ValueError: If the data set is not set.

        Returns:
            str: The data type of the column.
        """
        if self.data_set is None:
            raise ValueError("DataSet is not set")
        return self.data_set.data_schema[self.name]

    @property
    def feature_importance(self) -> float:
        """Gets the feature importance for the column.

        Raises:
            ValueError: If the data_set is not set for the column.

        Returns:
            float: The feature importance for the column.
        """
        if self.data_set is None:
            raise ValueError("DataSet is not set")

        if self.role in (ColumnRole.FEATURE, ColumnRole.CATEGORICAL):
            return self.data_set.feature_importance[self.name]

        return -1

    @property
    def is_eligible_for_operation(self) -> bool:
        """Checks if the column is eligible for operation.

        Returns:
            bool: True if the column is eligible for operation, False otherwise.
        """

        if self._is_eligible_for_operation is not None:
            return self._is_eligible_for_operation

        if self.role in (
                ColumnRole.LABEL,
                ColumnRole.PREDICTION,
                ColumnRole.PROBABILITY_SCORE,
                ColumnRole.META_MODEL_TARGET,
                ColumnRole.META_MODEL_PROBABILITY_SCORE,
                ColumnRole.META_MODEL_CLASSIFICATION):
            self._is_eligible_for_operation = True
            return self._is_eligible_for_operation

        if self.role in (ColumnRole.FEATURE, ColumnRole.CATEGORICAL):
            column_operation_limit = ControlBoxManager().get_control_box().get_single_column_operation_limit()
            eligible_for_operation = list(
                self.data_set.feature_importance.keys())[
                :column_operation_limit]

            if self.name in eligible_for_operation:
                self._is_eligible_for_operation = True
                return self._is_eligible_for_operation

        self._is_eligible_for_operation = False
        return self._is_eligible_for_operation

    @is_eligible_for_operation.setter
    def is_eligible_for_operation(self, value: bool) -> None:
        self._is_eligible_for_operation = value

    @property
    def is_eligible_for_insights(self) -> bool:
        """Checks if the column is eligible for insights computation.

        Returns:
            bool: True if the column is eligible for insights computation. False otherwise.
        """

        if self._is_eligible_for_insights is not None:
            return self._is_eligible_for_insights

        if self.role in (
                ColumnRole.PREDICTION,
                ColumnRole.PROBABILITY_SCORE,
                ColumnRole.META_MODEL_TARGET,
                ColumnRole.META_MODEL_CLASSIFICATION):
            self._is_eligible_for_insights = True
            return self._is_eligible_for_insights

        if self.role in (ColumnRole.FEATURE, ColumnRole.CATEGORICAL):
            column_operation_limit = ControlBoxManager().get_control_box().get_two_column_operation_limit()
            eligible_for_operation = list(
                self.data_set.feature_importance.keys())[
                :column_operation_limit]

            self._is_eligible_for_insights = self.name in eligible_for_operation
            return self._is_eligible_for_insights

        self._is_eligible_for_insights = False
        return self._is_eligible_for_insights

    @is_eligible_for_insights.setter
    def is_eligible_for_insights(self, value: bool) -> None:
        self._is_eligible_for_insights = value

    @property
    def is_eligible_for_data_quality(self) -> bool:
        if self._is_eligible_for_data_quality is not None:
            return self._is_eligible_for_data_quality

        if self.role in (ColumnRole.FEATURE, ColumnRole.CATEGORICAL):
            column_data_quality_limit = ControlBoxManager().get_control_box().get_single_column_operation_limit()
            eligible_for_data_quality = list(
                self.data_set.feature_importance.keys())[:column_data_quality_limit]

            if self.name in eligible_for_data_quality:
                self._is_eligible_for_data_quality = True
                return self._is_eligible_for_data_quality

        self._is_eligible_for_data_quality = False
        return self._is_eligible_for_data_quality

    @is_eligible_for_data_quality.setter
    def is_eligible_for_data_quality(self, value: bool) -> None:
        self._is_eligible_for_data_quality = value

    @property
    def distinct_count_query(self) -> str:
        """Returns the query to count the distinct rows for the given column.

        Returns:
            str: The query to count the distinct rows for the given column.
        """

        return f"SELECT COUNT(DISTINCT \"{self.name}\") FROM {self.data_set.full_table_name}"

    def set_data_set(self, data_set) -> None:
        self.data_set = DataColumn.DataSetTuple(
            data_set.id,
            data_set.count,
            data_set.data_schema,
            data_set.problem_type,
            data_set.feature_importance,
            getattr(data_set, "dialect", None),
            getattr(data_set, "full_table_name", None))

    async def count_distinct_rows(self, data: Union[pd.DataFrame, sqlalchemy.engine.base.Engine]) -> int:
        """Counts the distinct rows for the given column.

        Args:
            data (Union[pd.DataFrame, sqlalchemy.engine.base.Engine]): The data to count the distinct rows for.

        Raises:
            Exception: If there is an error while executing the query.

        Returns:
            int: The number of distinct rows.
        """
        if isinstance(data, pd.DataFrame):
            return await asyncify_fn(data[self.name].nunique)

        count = await execute_count_query(query=self.distinct_count_query, data=data)
        return count

    async def compute_stats(self,
                            data: Union[pd.DataFrame,
                                        sqlalchemy.engine.base.Engine]) -> None:
        """Computes the stats for the given column.

        Args:
            data (Union[pd.DataFrame, sqlalchemy.engine.base.Engine]): The data to compute the stats for.
        """
        if not self.is_eligible_for_operation and not self.is_eligible_for_insights:
            return

        self.distinct_count = await self.count_distinct_rows(data)

    def to_dict(self) -> Dict:
        """Converts the object to a dictionary.

        Returns:
            Dict: The dictionary representation of the object.
        """
        return {
            "name": self.name,
            "role": self.role.value,
            "type": self.type.value
        }

    @classmethod
    def from_dict(cls, dict_: Dict) -> "DataColumn":
        """Constructs a DataColumn object from a dictionary.

        The returned object will be of a type that matches the dictionary's
        type key. The default object type is of DataColumn

        Args:
            dict_ (Dict): A dictionary containing the column information.

        Raises:
            ValueError: If there are any missing or invalid values in the dictionary.

        Returns:
            DataColumn: A DataColumn object.
        """
        try:
            if dict_["type"] == ColumnType.CATEGORICAL.value:
                from ibm_metrics_plugin.metrics.drift_v2.entity.column.categorical_column import \
                    CategoricalColumn
                return CategoricalColumn.from_dict(dict_)

            if dict_["type"] == ColumnType.NUMERICAL.value:
                from ibm_metrics_plugin.metrics.drift_v2.entity.column.numerical_column import \
                    NumericalColumn
                return NumericalColumn.from_dict(dict_)

            if dict_["type"] == ColumnType.PROBABILITY.value:
                from ibm_metrics_plugin.metrics.drift_v2.entity.column.probability_column import \
                    ProbabilityColumn
                return ProbabilityColumn.from_dict(dict_)

            column = cls(dict_["name"], ColumnRole(dict_["role"]))
            column.type = ColumnType(dict_["type"])
            column.is_eligible_for_data_quality = dict_.get("is_eligible_for_data_quality", False)
            column.is_eligible_for_operation = dict_.get("is_eligible_for_operation", False)
            column.is_eligible_for_insights = dict_.get("is_eligible_for_insights", False)
            return column
        except KeyError as e:
            raise ValueError(
                f"Cannot create a data column from the given dictionary. Missing key {e}.") from e

    @classmethod
    def copy_from(cls, other: "DataColumn") -> "DataColumn":
        from ibm_metrics_plugin.metrics.drift_v2.entity.column.categorical_column import \
            CategoricalColumn
        from ibm_metrics_plugin.metrics.drift_v2.entity.column.numerical_column import \
            NumericalColumn
        if isinstance(other, CategoricalColumn):
            column = CategoricalColumn(other.name, other.role)
        elif isinstance(other, NumericalColumn):
            column = NumericalColumn(other.name, other.role)
            column.is_discrete = other.is_discrete
        else:
            column = DataColumn(other.name, other.role)

        return column

    def __lt__(self, other: "DataColumn") -> bool:
        # We need to do this in priority, so that we don't have to dynamically generate some statistics later.
        # Priority for source columns
        # 1. META_MODEL_TARGET_COLUMN
        # 2. META_MODEL_CLASSIFICATION_COLUMN if available
        # 3. Prediction Column
        # 4. Label Column if available
        # 5. Categorical Columns in order of feature importance
        # 6. Probability Columns if available
        # 7. Numerical Columns in order of feature importance

        if (self.role is ColumnRole.CATEGORICAL and other.role is ColumnRole.CATEGORICAL) or (
                self.role is ColumnRole.FEATURE and other.role is ColumnRole.FEATURE):
            f1 = self.data_set.feature_importance.get(self.name, 0)
            f2 = self.data_set.feature_importance.get(other.name, 0)

            # If both feature importances are same, sort them alphabetically
            # Else sort them by feature importance
            return self.name < other.name if (f1 == f2) else f1 < f2

        if self.role is ColumnRole.PROBABILITY_SCORE and other.role is ColumnRole.PROBABILITY_SCORE:
            # Both are probability score columns. Doesn't matter which comes first.
            # Sort based on the names
            return self.name < other.name

        # Role priority is defined in ColumnRole enum
        return self.role < other.role

    def __eq__(self, other: "DataColumn") -> bool:
        if other is None:
            return False
        return (self.name == other.name)
