
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
from ibm_metrics_plugin.metrics.drift_v2.entity.column.probability_column import \
    ProbabilityColumn
from ibm_metrics_plugin.metrics.drift_v2.entity.statistics.continuous_statistics import \
    ContinuousStatistics
from ibm_metrics_plugin.metrics.drift_v2.entity.statistics.statistics import \
    Statistics
from ibm_metrics_plugin.metrics.drift_v2.entity.statistics.element import \
    ContinuousElement
from ibm_metrics_plugin.metrics.drift_v2.entity.operation.operation import \
    Operation
from ibm_metrics_plugin.metrics.drift_v2.utils.constants import OperationKind
from ibm_metrics_plugin.metrics.drift_v2.utils.drift_utils import \
    get_logging_params

logger = MetricLogger(__name__)


class ContinuousFeatureCountsOperation(Operation):
    """
        This operation divides a continuous column into bins and counts
        the number of times each bin occurs.
    """

    def __init__(self):
        super().__init__(kind=OperationKind.CONTINUOUS_FEATURE_COUNTS)

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
        return f"Continuous Feature Counts for {self.target_column.name}"

    @property
    def description(self) -> str:
        """Returns the description of the operation.

        Returns:
            str: The description of the operation.
        """
        # TODO Improve the message
        return f"This operation counts the number of times each value in the column {self.target_column.name} occurs."

    @property
    def query(self) -> str:
        """Returns the query to divide the column into bins and count the number of times each bin occurs.

        Returns:
            str: The query
        """
        if isinstance(self.target_column, ProbabilityColumn):
            new_column = f"FLOOR((tmp.probability - {self.target_column.min_})/{self.target_column.bin_width})"
            op_query = f"SELECT {new_column} AS \"bin\", COUNT(*) AS \"count\""
            op_query += f" FROM {self.target_column.sub_query()} GROUP BY {new_column}"

            # There is no 'where sub clause' in ProbabilityColumn because this is not
            # present at payload time.
            return op_query

        new_column = f"FLOOR((\"{self.target_column.name}\" - {self.target_column.min_})/{self.target_column.bin_width})"
        op_query = f"SELECT {new_column} AS \"bin\", COUNT(*) AS \"count\""
        op_query += f" FROM {self.data_set.full_table_name}"
        op_query += f" GROUP BY {new_column}"

        return op_query

    def execute_pandas(self, data: pd.DataFrame) -> Dict[str, Statistics]:
        """Executes the operation on a pandas dataframe.

        Args:
            data (pd.DataFrame): The dataframe to execute the operation on.

        Returns:
            Dict[str, Statistics]: The result of the operation.
        """
        start_time = time()
        counts = (data[self.target_column.name] - self.target_column.min_) / \
            self.target_column.bin_width
        counts = counts.dropna().astype(int).value_counts()
        counts.index = counts.index * self.target_column.bin_width + self.target_column.min_
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

        # TODO Think of a better way
        counts.dropna(subset=["bin"], inplace=True)

        counts.set_index("bin", inplace=True)
        counts.index = counts.index.astype(
            int) * self.target_column.bin_width + self.target_column.min_
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
        statistics = ContinuousStatistics(target_column=self.target_column.name,
                                              bin_width=self.target_column.bin_width,
                                              is_integer=(self.target_column.data_type == "int"))

        for index, count in zip(counts.index, counts):
            statistics.add_element(ContinuousElement(index, count))

        statistics.compute_summary()
        return {statistics.name: statistics}

    async def execute(self,
                data: Union[pd.DataFrame,
                            sqlalchemy.engine.base.Engine]) -> Dict[str, Statistics]:
        """Executes the operation.

        Args:
            data (Union[pd.DataFrame, sqlalchemy.engine.base.Engine]): The data to execute the operation on.
            column (DataColumn): The column to execute the operation on.

        Returns:
            Dict[str, Statistics]: The result of the operation.
        """
        if isinstance(data, pd.DataFrame):
            self.statistics.update(self.execute_pandas(data))

        if isinstance(data, sqlalchemy.engine.base.Engine):
            self.statistics.update(await self.execute_query(data))
