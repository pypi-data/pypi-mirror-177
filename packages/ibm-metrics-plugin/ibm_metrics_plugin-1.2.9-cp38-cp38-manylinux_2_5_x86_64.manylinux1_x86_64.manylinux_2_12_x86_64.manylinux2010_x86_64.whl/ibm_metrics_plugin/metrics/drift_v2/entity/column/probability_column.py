# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2022
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------


from typing import Dict, List, Union

import sqlalchemy
from ibm_metrics_plugin.metrics.drift_v2.entity.column.numerical_column import \
    NumericalColumn
from ibm_metrics_plugin.metrics.drift_v2.utils.async_utils import asyncify_fn
from ibm_metrics_plugin.metrics.drift_v2.utils.constants import (
    PROBABILITY_COLUMN_TEMPLATE, ColumnRole, ColumnType)


class ProbabilityColumn(NumericalColumn):
    def __init__(self,
                 prediction: Union[str, int, float]) -> None:
        name = PROBABILITY_COLUMN_TEMPLATE.substitute(prediction=prediction)
        super().__init__(name, ColumnRole.PROBABILITY_SCORE)

        self.type = ColumnType.PROBABILITY
        self.prediction = prediction
        self.probability_column = None
        self.predicted_labels = []
        self._is_discrete = False

    def sub_query(self, other_column: str = None) -> str:
        """Computes the sub query to separate the probabilities in the probability column.

        Currently only supports DB2 and Postgres. Not tested on other databases.

        Raises:
            Exception: The dialect is not set or not supported.

        Returns:
            str: The sub query to separate the probabilities in the probability column.
        """
        if self.data_set.dialect is None:
            raise Exception("Dialect not set")

        probability_index = self.predicted_labels.index(self.prediction)
        query = ""

        if "ibm" in self.data_set.dialect:
            if other_column:
                query = f"(SELECT \"{other_column}\", JSON_VALUE(\"{self.probability_column}\", '$.{probability_index}' returning float)"
            else:
                query = f"(SELECT JSON_VALUE(\"{self.probability_column}\", '$.{probability_index}' returning float)"

        elif "postgresql" in self.data_set.dialect:
            if other_column:
                query = f"(SELECT \"{other_column}\", (\"{self.probability_column}\"->{probability_index})::float"
            else:
                query = f"(SELECT (\"{self.probability_column}\"->{probability_index})::float"

        else:
            raise Exception(f"Dialect {self.data_set.dialect} not supported")

        query += f" AS probability FROM {self.data_set.full_table_name}) tmp"
        return query

    @property
    def summary_query(self) -> str:
        """This query is used to compute the summary stats for the column.

        The stats computed are: min, max, mean, std

        Returns:
            str: The summary query for the given column.
        """
        query = f"SELECT MIN(tmp.probability) AS \"min\", MAX(tmp.probability) AS \"max\","
        query += f" AVG(tmp.probability) AS \"mean\", STDDEV(tmp.probability) AS \"std\""
        query += f" FROM {self.sub_query()}"

        return query

    def percentile_query(self, percentile_array: List[float]) -> str:
        """Computes the percentile query for the given column.

        Args:
            percentile_array (List[float]): The array of values to compute percentiles.

        Returns:
            str: The percentile query for the given column.
        """
        query = []
        for percentile in percentile_array:
            query.append(
                f" PERCENTILE_CONT({percentile}) WITHIN GROUP (ORDER BY tmp.probability) AS \"{percentile}\"")

        query = "SELECT " + ",".join(query)
        query += f" FROM {self.sub_query()}"

        return query

    async def count_distinct_rows(self, data: sqlalchemy.engine.base.Engine) -> int:
        """Counts the number of distinct rows in the data set.
        This currently only returns -1. This is because this computation for
        probability column is not required.

        Args:
            data (sqlalchemy.engine.base.Engine): The data set.

        Returns:
            int: The number of distinct rows in the data set. Always return -1.
        """
        def fn(): return -1
        return await asyncify_fn(fn)

    def set_probability_column(self, probability_column: str) -> None:
        """Sets the probability column.

        Args:
            probability_column (str): The probability column.

        """
        self.probability_column = probability_column

    def set_predicted_labels(self, predicted_labels: List[str]) -> None:
        """Sets the predicted labels.

        Args:
            predicted_labels (List[str]): The predicted labels.
        """
        self.predicted_labels = predicted_labels

    def to_dict(self) -> Dict:
        """Converts the object to a dictionary.

        Returns:
            Dict: The dictionary representation of the object.
        """
        dict_ = super().to_dict()
        dict_.update({
            "prediction": self.prediction
        })
        return dict_

    @classmethod
    def from_dict(cls, dict_: Dict) -> "ProbabilityColumn":
        """Constructs a ProbabilityColumn object from a dictionary.

        Args:
            dict_ (Dict): A dictionary containing the column information.

        Raises:
            ValueError: If there are any missing or invalid values in the dictionary.

        Returns:
            ProbabilityColumn: A ProbabilityColumn object.
        """
        try:
            column = cls(dict_["prediction"])

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
