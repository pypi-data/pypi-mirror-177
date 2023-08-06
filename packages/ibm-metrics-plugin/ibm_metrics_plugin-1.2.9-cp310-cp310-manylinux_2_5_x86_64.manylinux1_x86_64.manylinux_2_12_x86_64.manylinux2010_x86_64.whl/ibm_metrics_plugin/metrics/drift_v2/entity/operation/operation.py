# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2022
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

from abc import abstractmethod
from typing import List, NamedTuple, Union

import pandas as pd
import sqlalchemy
from ibm_metrics_plugin.metrics.drift_v2.entity.column.categorical_column import \
    CategoricalColumn
from ibm_metrics_plugin.metrics.drift_v2.entity.column.data_column import \
    DataColumn
from ibm_metrics_plugin.metrics.drift_v2.entity.column.numerical_column import \
    NumericalColumn
from ibm_metrics_plugin.metrics.drift_v2.entity.statistics.continuous_statistics import \
    ContinuousStatistics
from ibm_metrics_plugin.metrics.drift_v2.entity.statistics.discrete_statistics import \
    DiscreteStatistics
from ibm_metrics_plugin.metrics.drift_v2.entity.statistics.statistics import \
    Statistics
from ibm_metrics_plugin.metrics.drift_v2.utils.constants import (DataSetType,
                                                                 OperationKind)


class Operation:
    """
    Operations
        - [x] DiscreteFeatureCountsOperation
        - [x] ContinuousFeatureCountsOperation
        - [x] Discrete_DiscreteFeatureCountsOperation
        - [x] Discrete_ContinuousFeatureCountsOperation
        - [] Continuous_ContinuousFeatureCountsOperation
    """

    DataSetTuple = NamedTuple("data_set",
                              [("id", str),
                               ("count", int),
                               ("type", DataSetType),
                               ("full_table_name", str)])

    def __init__(self, kind: OperationKind):
        self.kind = kind
        self.statistics = {}
        self.data_set = None
        self.target_column = None
        self.source_column = None

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError()

    @property
    def file_name(self) -> str:
        """Returns the file name for the operation.

        Returns:
            str: The file name for the operation.
        """

        return f"{self.name}.json"

    @property
    @abstractmethod
    def display_name(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def description(self) -> str:
        raise NotImplementedError()

    def set_data_set(self, data_set) -> None:
        self.data_set = Operation.DataSetTuple(
            data_set.id,
            data_set.count,
            data_set.type,
            getattr(data_set, "full_table_name", None))

    @classmethod
    def factory(cls, target_column: DataColumn, source_column: DataColumn = None) -> "Operation":
        """Factory method to create an operation.

        Args:
            target_column (DataColumn): Column to be used for the operation.

        Returns:
            Operation: The operation.
        """
        from ibm_metrics_plugin.metrics.drift_v2.entity.operation.continuous_feature_counts_operation import \
            ContinuousFeatureCountsOperation
        from ibm_metrics_plugin.metrics.drift_v2.entity.operation.discrete_continuous_feature_counts_operation import \
            DiscreteContinuousFeatureCountsOperation
        from ibm_metrics_plugin.metrics.drift_v2.entity.operation.discrete_discrete_feature_counts_operation import \
            DiscreteDiscreteFeatureCountsOperation
        from ibm_metrics_plugin.metrics.drift_v2.entity.operation.discrete_feature_counts_operation import \
            DiscreteFeatureCountsOperation

        if isinstance(target_column, CategoricalColumn):
            operation = DiscreteFeatureCountsOperation() \
                if source_column is None else DiscreteDiscreteFeatureCountsOperation()
        elif isinstance(target_column, NumericalColumn) and target_column.is_discrete:
            operation = DiscreteFeatureCountsOperation() \
                if source_column is None else DiscreteDiscreteFeatureCountsOperation()
        else:
            operation = ContinuousFeatureCountsOperation() \
                if source_column is None else DiscreteContinuousFeatureCountsOperation()

        operation.target_column = target_column
        operation.source_column = source_column
        return operation

    @classmethod
    def copy_from(cls, other: "Operation"):
        from ibm_metrics_plugin.metrics.drift_v2.entity.operation.continuous_feature_counts_operation import \
            ContinuousFeatureCountsOperation
        from ibm_metrics_plugin.metrics.drift_v2.entity.operation.discrete_continuous_feature_counts_operation import \
            DiscreteContinuousFeatureCountsOperation
        from ibm_metrics_plugin.metrics.drift_v2.entity.operation.discrete_discrete_feature_counts_operation import \
            DiscreteDiscreteFeatureCountsOperation
        from ibm_metrics_plugin.metrics.drift_v2.entity.operation.discrete_feature_counts_operation import \
            DiscreteFeatureCountsOperation
        if other.kind == OperationKind.DISCRETE_FEATURE_COUNTS:
            return DiscreteFeatureCountsOperation()
        elif other.kind == OperationKind.CONTINUOUS_FEATURE_COUNTS:
            return ContinuousFeatureCountsOperation()
        elif other.kind == OperationKind.DISCRETE_CONTINUOUS_FEATURE_COUNTS:
            return DiscreteContinuousFeatureCountsOperation()
        elif other.kind == OperationKind.DISCRETE_DISCRETE_FEATURE_COUNTS:
            return DiscreteDiscreteFeatureCountsOperation()
        else:
            # Should not reach here
            raise ValueError("Not a supported operation.")

    @abstractmethod
    async def execute(self,
                data: Union[pd.DataFrame,
                            sqlalchemy.engine.base.Engine]) -> List[Statistics]:
        """Default execute method for all operations.

        Args:
            data (Union[pd.DataFrame, sqlalchemy.engine.base.Engine]): Data to be used for the operation.

        Returns:
            List[Statistics]: The result of the operation.
        """
        raise NotImplementedError()

    def to_dict(self) -> dict:
        """Converts the operation to a dictionary.

        Returns:
            dict: The operation as a dictionary.
        """
        if self.data_set is None:
            raise ValueError("Operation data set is not set.")

        dict_ = {
            "name": self.name,
            "display_name": self.display_name,
            "description": self.description,
            "kind": self.kind.value,
            "computed_on": {
                "data_set_name": self.data_set.type.value,
                "data_set_id": self.data_set.id,
                "target_column": self.target_column.name},
            "statistics": {
                statistics.name: statistics.to_dict() for statistics in self.statistics.values()
            }
        }

        if self.source_column is not None:
            dict_["computed_on"]["source_column"] = self.source_column.name

        return dict_

    def to_summary_dict(self) -> dict:
        """Converts the operation to a dictionary to be included in summary.json

        Returns:
            dict: The operation as a dictionary
        """
        dict_ = {
            "name": self.name,
            "kind": self.kind.value,
            "target_column": self.target_column.name,
            "file_name": self.file_name
        }

        if self.source_column is not None:
            dict_["source_column"] = self.source_column.name
        return dict_

    @classmethod
    def from_dict(cls, dict_: dict) -> "Operation":
        from ibm_metrics_plugin.metrics.drift_v2.entity.operation.continuous_feature_counts_operation import \
            ContinuousFeatureCountsOperation
        from ibm_metrics_plugin.metrics.drift_v2.entity.operation.discrete_continuous_feature_counts_operation import \
            DiscreteContinuousFeatureCountsOperation
        from ibm_metrics_plugin.metrics.drift_v2.entity.operation.discrete_discrete_feature_counts_operation import \
            DiscreteDiscreteFeatureCountsOperation
        from ibm_metrics_plugin.metrics.drift_v2.entity.operation.discrete_feature_counts_operation import \
            DiscreteFeatureCountsOperation
        try:
            operation = None
            if dict_["kind"] == OperationKind.DISCRETE_FEATURE_COUNTS.value:
                operation = DiscreteFeatureCountsOperation()
                for id, statistics in dict_["statistics"].items():
                    operation.statistics[id] = DiscreteStatistics.from_dict(statistics)
            elif dict_["kind"] == OperationKind.CONTINUOUS_FEATURE_COUNTS.value:
                operation = ContinuousFeatureCountsOperation()
                for id, statistics in dict_["statistics"].items():
                    operation.statistics[id] = ContinuousStatistics.from_dict(statistics)
            elif dict_["kind"] == OperationKind.DISCRETE_CONTINUOUS_FEATURE_COUNTS.value:
                operation = DiscreteContinuousFeatureCountsOperation()
                for id, statistics in dict_["statistics"].items():
                    operation.statistics[id] = ContinuousStatistics.from_dict(statistics)
            elif dict_["kind"] == OperationKind.DISCRETE_DISCRETE_FEATURE_COUNTS.value:
                operation = DiscreteDiscreteFeatureCountsOperation()
                for id, statistics in dict_["statistics"].items():
                    operation.statistics[id] = DiscreteStatistics.from_dict(statistics)

            return operation

        except KeyError as e:
            raise ValueError(
                f"Cannot create an operation from the given dictionary. Missing key {e}.") from e
