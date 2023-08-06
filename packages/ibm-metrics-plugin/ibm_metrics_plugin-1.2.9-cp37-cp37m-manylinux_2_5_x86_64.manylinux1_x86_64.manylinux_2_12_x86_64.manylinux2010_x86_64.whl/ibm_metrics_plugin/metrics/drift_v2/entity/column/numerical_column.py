# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2022
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

from time import time
from typing import Dict, List, Union

import numpy as np
import pandas as pd
import sqlalchemy
from ibm_metrics_plugin.clients.readers.async_query_executor import \
    execute_query
from ibm_metrics_plugin.common.utils.metrics_logger import MetricLogger
from ibm_metrics_plugin.common.utils.python_utils import get_python_types
from ibm_metrics_plugin.metrics.drift_v2.entity.column.data_column import \
    DataColumn
from ibm_metrics_plugin.metrics.drift_v2.utils.constants import (ColumnRole,
                                                                 ColumnType)
from ibm_metrics_plugin.metrics.drift_v2.utils.drift_utils import \
    get_logging_params

logger = MetricLogger(__name__)


class NumericalColumn(DataColumn):
    def __init__(self, name: str, role: ColumnRole) -> None:
        super().__init__(name, role)

        self.type = ColumnType.NUMERICAL
        self.percentiles = {}
        self.min_ = None
        self.max_ = None
        self.mean = None
        self.std = None
        self.bin_width = 0
        self.iqr = None
        self._is_discrete = None

    @property
    def is_discrete(self) -> bool:
        """Check if the column is discrete.

        Raises:
            Exception: The distinct count is not set for this column.

        Returns:
            bool: True if the column is discrete, False otherwise.
        """

        if self._is_discrete is None:
            if self.distinct_count is None:
                raise Exception(f"Distinct Count is not set for {self.name}")
            self._is_discrete = self.distinct_count <= np.round(np.log2(self.count))

        return self._is_discrete

    @is_discrete.setter
    def is_discrete(self, flag: bool) -> None:
        self._is_discrete = flag

    @property
    def summary_query(self) -> str:
        """This query is used to compute the summary stats for the column.

        The stats computed are: min, max, mean, std

        Returns:
            str: The summary query for the given column.
        """

        query = f"SELECT MIN(\"{self.name}\") AS \"min\", MAX(\"{self.name}\") AS \"max\", "
        query += f"AVG(\"{self.name}\") AS \"mean\", STDDEV(\"{self.name}\") AS \"std\" "
        query += f"FROM {self.data_set.full_table_name}"
        return query

    def percentile_query(self, percentile_array: List[float]) -> str:
        """Computes the percentile query for the given column.

        Args:
            percentile_array (List[float]): The array of values to compute percentiles.

        Returns:
            str: The percentile query for the given column.
        """
        # PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY LOANAMOUNT) AS "0.25"
        query = []
        for percentile in percentile_array:
            query.append(
                f" PERCENTILE_CONT({percentile}) WITHIN GROUP (ORDER BY \"{self.name}\") AS \"{percentile}\"")

        query = "SELECT " + ",".join(query) + f" FROM {self.data_set.full_table_name}"
        return query

    def outlier_query(self, lower_limit: Union[int, float], upper_limit: Union[int, float]) -> str:
        """Computes the outlier count query for the given column

        Args:
            lower_limit (Union[int, float]): The lower limit for outlier
            upper_limit (Union[int, float]): The upper limit for outlier

        Returns:
            str: The outlier query for the given column.
        """
        # select count("AGE") from "Payload_ad90f055-a83c-410e-afe0-8e85de65211f"
        # where "AGE" < 30 or "AGE" > 60;
        query = f"SELECT COUNT(\"{self.name}\") AS \"count\" "
        query += f"FROM {self.data_set.full_table_name}"

        conditions_str = f"(\"{self.name}\" < {lower_limit} OR \"{self.name}\" > {upper_limit})"

        query += f" WHERE {conditions_str}"

        return query

    def compute_percentiles(self,
                            data: Union[pd.DataFrame, sqlalchemy.engine.base.Engine],
                            percentile_array: List = [0.25, 0.5, 0.75]) -> dict:
        """Computes the percentiles for the given column.

        Args:
            data (Union[pd.DataFrame, sqlalchemy.engine.base.Engine]): The data to compute the percentiles for.
            percentile_array (List, optional): The array of values to compute percentiles. Defaults to [0.25, 0.5, 0.75].

        Raises:
            Exception: If there is an error while executing the query.

        Returns:
            dict: The percentiles for the given column.
        """
        if isinstance(data, pd.DataFrame):
            start_time = time()
            self.percentiles.update(data[self.name].quantile(percentile_array).to_dict())
            logger.log_info(
                f"Updated {percentile_array} in percentiles.",
                get_logging_params(
                    column=self,
                    start_time=start_time))
            return

        try:
            start_time = time()
            query = self.percentile_query(percentile_array)
            with data.connect() as conn:
                logger.log_info(
                    f"Executing percentile query for {percentile_array} percentiles.",
                    get_logging_params(
                        column=self,
                        query=query))
                percentiles = pd.read_sql(query, conn).T.squeeze()
                logger.log_info(
                    f"Executed percentile query for {percentile_array} percentiles.",
                    get_logging_params(
                        column=self,
                        query=query,
                        start_time=start_time))
                logger.log_info(
                    f"Updated {percentile_array} in percentiles.",
                    get_logging_params(
                        column=self,
                        start_time=start_time))
                self.percentiles.update(dict(zip(percentile_array, percentiles)))
        except sqlalchemy.exc.SQLAlchemyError as e:
            raise Exception(
                f"Got an error while executing the query {query}") from e

    def compute_bin_width(self, data: Union[pd.DataFrame, sqlalchemy.engine.base.Engine]) -> None:
        """Computes the bin width for the given column.
        """
        self.iqr = self.percentiles[0.75] - self.percentiles[0.25]

        if self.iqr > 0:
            self.bin_width = 2 * self.iqr / np.power(self.count, 1 / 3)
        else:
            h = 1 / 8
            min_h = 1 / 64
            while h > min_h:
                percentile_array = [h, 1 - h]
                logger.log_info(
                    f"IQR = {self.iqr}, Trying to find with {percentile_array} percentiles",
                    get_logging_params(
                        column=self))
                self.compute_percentiles(data, percentile_array=percentile_array)

                self.iqr = self.percentiles[1 - h] - self.percentiles[h]
                if self.iqr > 0:
                    self.bin_width = 2 * self.iqr / np.power(self.count, 1 / 3)
                    break
                h = h / 2

        if self.bin_width == 0:
            logger.log_info(
                f"Bin Width is 0. Disabling operations and insights.",
                get_logging_params(
                    column=self))
            self.is_eligible_for_operation = False
            self.is_eligible_for_insights = False

            # Right now data quality is tied to a feature drift.
            # If operation is disabled, disabling the data quality too.
            self.is_eligible_for_data_quality = False
            return

        self.bin_width = round(self.bin_width / 3, 8)
        if self.data_type == "int":
            # Doing `ceil` here instead of `floor` to auto-fix for cases when 0<bin_width<1
            self.bin_width = np.ceil(self.bin_width).astype(int)

    def compute_summary_stats_pandas(self, data: pd.DataFrame) -> None:
        """Computes the summary stats for the given column using Pandas.

        Args:
            data (pd.DataFrame): The data to compute the stats for.
        """
        self.min_ = data[self.name].min()
        self.max_ = data[self.name].max()
        self.mean = data[self.name].mean()
        self.std = data[self.name].std()
        self.compute_percentiles(data)

        if not self.is_discrete:
            self.compute_bin_width(data)

    async def compute_summary_stats_sql(self, data: sqlalchemy.engine.base.Engine) -> None:
        """Computes the summary stats for the given column using SQL.

        Args:
            data (sqlalchemy.engine.base.Engine): The data to compute the stats for.

        Raises:
            Exception: If there is an error while executing the query.
        """
        result = await execute_query(self.summary_query, data)
        summary = result.T.squeeze()

        self.min_ = summary["min"]
        self.max_ = summary["max"]
        self.mean = summary["mean"]
        self.std = summary["std"]
        self.compute_percentiles(data)

        if not self.is_discrete:
            self.compute_bin_width(data)

    async def compute_stats(self,
                            data: Union[pd.DataFrame,
                                        sqlalchemy.engine.base.Engine]) -> None:
        """Computes the stats for the given column.

        Args:
            data (Union[pd.DataFrame, sqlalchemy.engine.base.Engine]): The data to compute the stats for.
        """
        if not self.is_eligible_for_operation and not self.is_eligible_for_insights:
            return

        await super().compute_stats(data)

        if isinstance(data, pd.DataFrame):
            self.compute_summary_stats_pandas(data)
        else:
            await self.compute_summary_stats_sql(data)

    def to_dict(self) -> Dict:
        """Converts the object to a dictionary.

        Returns:
            Dict: The dictionary representation of the object.
        """
        dict_ = {
            "name": self.name,
            "type": self.type.value,
            "role": self.role.value,
            "data_type": self.data_type,
            "feature_importance": get_python_types(self.feature_importance),
            "is_eligible_for_data_quality": self.is_eligible_for_data_quality,
            "is_eligible_for_operation": self.is_eligible_for_operation,
            "is_eligible_for_insights": self.is_eligible_for_insights,
        }

        if self.distinct_count is not None:
            dict_["distinct_count"] = get_python_types(self.distinct_count)
            dict_["is_discrete"] = get_python_types(self.is_discrete)

        if self.min_ is not None:
            dict_["min"] = get_python_types(self.min_)

        if self.max_ is not None:
            dict_["max"] = get_python_types(self.max_)

        if self.mean is not None:
            dict_["mean"] = get_python_types(self.mean)

        if self.std is not None:
            dict_["std"] = get_python_types(self.std)

        if self.percentiles:
            dict_["percentiles"] = get_python_types(self.percentiles)

        if self.bin_width is not None:
            dict_["bin_width"] = get_python_types(self.bin_width)

        if self.iqr is not None:
            dict_["iqr"] = get_python_types(self.iqr)

        return dict_

    @classmethod
    def from_dict(cls, dict_: Dict) -> "NumericalColumn":
        """Constructs a NumericalColumn object from a dictionary.

        Args:
            dict_ (Dict): A dictionary containing the column information.

        Raises:
            ValueError: If there are any missing or invalid values in the dictionary.

        Returns:
            NumericalColumn: A NumericalColumn object.
        """
        try:
            column = cls(name=dict_["name"], role=ColumnRole(dict_["role"]))

            column.distinct_count = dict_.get("distinct_count")
            column.min_ = dict_.get("min")
            column.max_ = dict_.get("max")
            column.mean = dict_.get("mean")
            column.std = dict_.get("std")
            column.bin_width = dict_.get("bin_width")
            column.iqr = dict_.get("iqr")
            column.percentiles = dict_.get("percentiles")

            column.is_eligible_for_data_quality = dict_.get("is_eligible_for_data_quality", False)
            column.is_eligible_for_operation = dict_.get("is_eligible_for_operation", False)
            column.is_eligible_for_insights = dict_.get("is_eligible_for_insights", False)

            return column
        except KeyError as e:
            raise ValueError(
                f"Cannot create a data column from the given dictionary. Missing key {e}.") from e
