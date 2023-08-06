# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2022
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

from time import time
from typing import Dict, Union

import pandas as pd
import sqlalchemy
from ibm_metrics_plugin.clients.readers.async_query_executor import execute_query
from ibm_metrics_plugin.common.utils.metrics_logger import MetricLogger
from ibm_metrics_plugin.metrics.drift_v2.entity.column.meta_model_classification_column import \
    MetaModelClassificationColumn
from ibm_metrics_plugin.metrics.drift_v2.entity.statistics.discrete_statistics import \
    DiscreteStatistics
from ibm_metrics_plugin.metrics.drift_v2.entity.statistics.statistics import \
    Statistics
from ibm_metrics_plugin.metrics.drift_v2.entity.statistics.element import \
    DiscreteElement
from ibm_metrics_plugin.metrics.drift_v2.entity.operation.operation import \
    Operation
from ibm_metrics_plugin.metrics.drift_v2.utils.constants import (DataSetType,
                                                                 OperationKind)
from ibm_metrics_plugin.metrics.drift_v2.utils.control_box import \
    ControlBoxManager
from ibm_metrics_plugin.metrics.drift_v2.utils.drift_utils import \
    get_logging_params

logger = MetricLogger(__name__)


class DiscreteFeatureCountsOperation(Operation):
    """
        This operation counts the number of times each value occurs in a
        discrete/categorical column.
    """

    def __init__(self):
        super().__init__(kind=OperationKind.DISCRETE_FEATURE_COUNTS)

    @property
    def name(self) -> str:
        """Returns the name of the operation.

        Returns:
            str: The name of the operation.
        """
        return f"{self.kind.value}_{self.target_column.name}"

    @property
    def display_name(self) -> str:
        """Returns the display name of the operation.

        Returns:
            str: The display name of the operation.
        """
        return f"Discrete Feature Counts for {self.target_column.name}"

    @property
    def description(self) -> str:
        """Returns the description of the operation.

        Returns:
            str: The description of the operation.
        """
        return f"This operation counts the number of times each value in the column {self.target_column.name} occurs."

    @property
    def query(self) -> str:
        """Returns the query to execute to do frequency count of a column.

        Returns:
            str: The query.
        """
        op_query = f"SELECT \"{self.target_column.name}\", COUNT(\"{self.target_column.name}\") AS \"count\""

        if isinstance(self.target_column, MetaModelClassificationColumn):
            op_query += f" FROM {self.target_column.sub_query()}"
        else:
            op_query += f" FROM {self.data_set.full_table_name}"

        op_query += f" GROUP BY \"{self.target_column.name}\""

        return op_query

    def execute_pandas(self, data: pd.DataFrame) -> Dict[str, Statistics]:
        """Executes the operation on a pandas dataframe.

        Args:
            data (pd.DataFrame): The dataframe to execute the operation on.

        Returns:
            Dict[str, Statistics]: The result of the operation.
        """

        if isinstance(self.target_column, MetaModelClassificationColumn):
            # This is not needed at the moment
            raise NotImplementedError

        start_time = time()
        counts = data[self.target_column.name].value_counts()
        statistics = self.__convert_counts_to_statistics(counts)
        logger.log_info(
            "Executed operation.",
            get_logging_params(
                start_time=start_time,
                operation=self))
        return statistics

    async def execute_query(self, data: sqlalchemy.engine.base.Engine) -> Dict[str, Statistics]:
        """Executes the operation on a sqlalchemy engine.

        Args:
            data (sqlalchemy.engine.base.Engine): The engine to execute the operation on.

        Returns:
            Dict[str, Statistics]: The result of the operation.
        """
        start_time = time()

        counts = await execute_query(query=self.query, data=data)
        counts.set_index(self.target_column.name, inplace=True)
        statistics = self.__convert_counts_to_statistics(counts["count"])
        logger.log_info(
            "Executed operation.",
            get_logging_params(
                start_time=start_time,
                operation=self))
        return statistics

    def __convert_counts_to_statistics(self, counts: pd.Series) -> Dict[str, Statistics]:
        """Converts a pandas series of counts to a list of statistics.

        Args:
            counts (pd.Series): The counts to convert.

        Returns:
            Dict[str, Statistics]: The converted statistics.
        """

        statistics = DiscreteStatistics(self.target_column.name)

        for index, count in zip(counts.index, counts):
            if index is None:
                continue
            statistics.add_element(DiscreteElement(index, count))

        # TODO Move the compute_buffer call outside the if block, if any production dataset
        # is to be used as baseline
        if self.data_set.type == DataSetType.BASELINE:
            statistics.compute_buffer()

        threshold = ControlBoxManager().get_control_box().get_discrete_discrete_operation_threshold()
        threshold = threshold * self.target_column.count
        if all(value < threshold for value in statistics.values):
            logger.log_info(
                f"Column has all values < {threshold}. Disabling insights.",
                get_logging_params(
                    operation=self))
            self.target_column.is_eligible_for_insights = False

        return {statistics.name: statistics}

    async def execute(self,
                data: Union[pd.DataFrame,
                            sqlalchemy.engine.base.Engine]) -> Dict[str, Statistics]:
        """Executes the operation.

        Args:
            data (Union[pd.DataFrame, sqlalchemy.engine.base.Engine]): The data to execute the operation on.

        Returns:
            Dict[str, Statistics]: The result of the operation.
        """

        if isinstance(data, pd.DataFrame):
            self.statistics.update(self.execute_pandas(data))

        elif isinstance(data, sqlalchemy.engine.base.Engine):
            self.statistics.update(await self.execute_query(data))
