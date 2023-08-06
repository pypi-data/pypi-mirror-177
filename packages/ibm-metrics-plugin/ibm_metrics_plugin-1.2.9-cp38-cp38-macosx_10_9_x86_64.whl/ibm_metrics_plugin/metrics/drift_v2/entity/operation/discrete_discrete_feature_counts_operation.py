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
from ibm_metrics_plugin.metrics.drift_v2.utils.constants import OperationKind
from ibm_metrics_plugin.metrics.drift_v2.utils.control_box import \
    ControlBoxManager
from ibm_metrics_plugin.metrics.drift_v2.utils.drift_utils import \
    get_logging_params

logger = MetricLogger(__name__)


class DiscreteDiscreteFeatureCountsOperation(Operation):
    """
        This operation counts the number of times each value occurs in a
        discrete/categorical column.
    """

    def __init__(self):
        super().__init__(kind=OperationKind.DISCRETE_DISCRETE_FEATURE_COUNTS)

    @property
    def name(self) -> str:
        """Returns the name of the operation.

        Returns:
            str: The name of the operation.
        """
        return f"{self.kind.value}_{self.source_column.name}_{self.target_column.name}"

    @property
    def display_name(self) -> str:
        """Returns the display name of the operation.

        Returns:
            str: The display name of the operation.
        """
        return f"Discrete Feature Counts for {self.target_column.name} for each feature value of {self.source_column.name}."

    @property
    def description(self) -> str:
        """Returns the description of the operation.

        Returns:
            str: The description of the operation.
        """
        return f"This operation counts the number of times each value in the column {self.target_column.name} occurs for each feature value of {self.source_column.name}."

    @property
    def query(self) -> str:
        """Returns the query to execute to do frequency count of a column.

        Returns:
            str: The query.
        """

        op_query = f"SELECT \"{self.source_column.name}\", \"{self.target_column.name}\", COUNT(\"{self.target_column.name}\") AS \"count\""

        if isinstance(self.source_column, MetaModelClassificationColumn):
            op_query += f" FROM {self.source_column.sub_query(self.target_column.name)}"
        else:
            op_query += f" FROM {self.data_set.full_table_name}"

        op_query += f" GROUP BY \"{self.source_column.name}\", \"{self.target_column.name}\""

        return op_query

    def execute_pandas(self, data: pd.DataFrame) -> Dict[str, Statistics]:
        """Executes the operation on a pandas dataframe.

        Args:
            data (pd.DataFrame): The dataframe to execute the operation on.

        Returns:
            Dict[str, Statistics]: The result of the operation.
        """

        start_time = time()
        counts = data.groupby([self.source_column.name,
                               self.target_column.name]).size().reset_index()
        counts.columns = [self.source_column.name, self.target_column.name, "count"]
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
        counts.columns = [self.source_column.name, self.target_column.name, "count"]
        statistics = self.__convert_counts_to_statistics(counts)
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

        count_statistics = {}
        threshold = ControlBoxManager().get_control_box(
        ).get_discrete_discrete_operation_threshold() * self.source_column.count
        for source_value in counts[self.source_column.name].unique():
            statistics = DiscreteStatistics(target_column=self.target_column.name,
                                                source_column=self.source_column.name,
                                                source_value=source_value)

            source_counts = counts[counts[self.source_column.name] == source_value]

            if source_counts["count"].sum() < threshold:
                continue

            def update_fn(row):
                if row[self.target_column.name] is not None:
                    return statistics.add_element(DiscreteElement(
                        row[self.target_column.name], row["count"]))

            _ = source_counts.apply(update_fn, axis=1)

            count_statistics[statistics.name] = statistics

        return count_statistics

    def create_statistics(self, value: str) -> Statistics:
        start_time = time()
        new_statistics = DiscreteStatistics(target_column=self.source_column.name,
                                                source_column=self.target_column.name,
                                                source_value=value)
        for statistics in self.statistics.values():
            try:
                element = statistics.get_element_by_field(value)
                new_element = DiscreteElement(statistics.source_value, element.value)
                new_statistics.add_element(new_element)
            except ValueError as ve:
                logger.log_warning(str(ve), get_logging_params(operation=self))
                new_element = DiscreteElement(statistics.source_value, 0)
                new_statistics.add_element(new_element)
                # TODO Should I eat up the error and return None?

        logger.log_info(
            "Created new statistics.",
            get_logging_params(
                operation=self,
                start_time=start_time))
        return new_statistics

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

        if isinstance(data, sqlalchemy.engine.base.Engine):
            self.statistics.update(await self.execute_query(data))
