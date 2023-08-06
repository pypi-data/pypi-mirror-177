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
import sklearn
from ibm_metrics_plugin.common.utils.metrics_logger import MetricLogger
from ibm_metrics_plugin.metrics.drift_v2.entity.accuracy.meta_model import \
    MetaModel
from ibm_metrics_plugin.metrics.drift_v2.entity.dataset.data_set import \
    DriftDataSet
from ibm_metrics_plugin.metrics.drift_v2.utils.constants import (
    META_MODEL_PROBABILITY_DIFF_COLUMN, META_MODEL_TARGET_COLUMN, RANDOM_SEED,
    MetaModelKind, PredictionClassification)
from ibm_metrics_plugin.metrics.drift_v2.utils.control_box import \
    ControlBoxManager
from ibm_metrics_plugin.metrics.drift_v2.utils.drift_utils import \
    get_logging_params
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder

logger = MetricLogger(__name__)

class HGBTMetaModel(MetaModel):
    def __init__(self) -> None:
        super().__init__(MetaModelKind.SKLEARN_HGBT)
        self.is_balanced_data = False
        self.is_optimised = False
        

    def fit(self, data: pd.DataFrame, data_set: DriftDataSet) -> None:
        start_time = time()
        if not(isinstance(data, pd.DataFrame)):
            raise ValueError("The training data is not of type pandas Dataframe.")
        
        self.feature_columns = [column.name for column in data_set.get_feature_columns()]

        input_df = data.copy(deep=True)

        self.probability_column = data_set.get_probability_column().name
        self.probability_score_columns = [
            column.name for column in data_set.get_probability_score_columns()]
        sorted_probabilities = np.sort(input_df[self.probability_score_columns].values)
        input_df[META_MODEL_PROBABILITY_DIFF_COLUMN] = sorted_probabilities[:, -1:] - \
            sorted_probabilities[:, -2:-1]

        self.feature_columns += self.probability_score_columns
        self.feature_columns += [META_MODEL_PROBABILITY_DIFF_COLUMN]

        self.categorical_columns = [column.name for column in data_set.get_categorical_columns()]

        train_y_df = input_df[META_MODEL_TARGET_COLUMN].replace(
            {PredictionClassification.CORRECT.value: 1, PredictionClassification.INCORRECT.value: 0})

        num_correct_predictions = sum(train_y_df)
        num_incorrect_predictions = len(train_y_df) - sum(train_y_df)

        logger.log_info(
            f"Correct Predictions: {num_correct_predictions}; Incorrect Predictions {num_incorrect_predictions}",
            get_logging_params(
                data_set=data_set))

        if num_incorrect_predictions == 0:
            error_message = "The client model seems to be over-fitted as there are no incorrect predictions."
            error_message += " Please retry this configuration after re-training client model."
            self.errors_map["no_incorrect_predictions"] = error_message
            logger.log_error(
                error_message,
                get_logging_params(
                    data_set=data_set,
                    start_time=start_time))
            return

        if num_correct_predictions == 0:
            error_message = "The client model seems to be under-fitted as there are no correct predictions."
            error_message += " Please retry this configuration after re-training client model."
            self.errors_map["no_correct_predictions"] = error_message
            logger.log_error(
                error_message,
                get_logging_params(
                    data_set=data_set,
                    start_time=start_time))
            return

        # Label encoding: Fit labels on entire dataset
        for feature in self.categorical_columns:
            le = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=np.nan)
            input_df = input_df.assign(
                **{feature: le.fit_transform(input_df[feature].values.reshape(-1, 1))})
            self.categorical_map[feature] = le.categories_[0]

        # Split 80 20
        train_df, test_df, train_y_df, test_y_df = train_test_split(
            input_df[self.feature_columns], train_y_df, test_size=0.2, stratify=train_y_df, random_state=RANDOM_SEED)
        train_df.reset_index(drop=True, inplace=True)
        test_df.reset_index(drop=True, inplace=True)
        train_y_df.reset_index(drop=True, inplace=True)
        test_y_df.reset_index(drop=True, inplace=True)

        self.base_client_accuracy = sum(test_y_df) / len(test_y_df)
        logger.log_info(
            f"Base Client accuracy: {self.base_client_accuracy:.2%}",
            get_logging_params(
                data_set=data_set))

        self._fit_without_optimise(train_df, train_y_df)

        if not self._check_accuracy(test_df):
            logger.log_info(
                f"Base Predicted accuracy: {self.base_predicted_accuracy:.2%}",
                get_logging_params(
                    data_set=data_set))

            error_message = "The meta model did not reach quality standards. Accuracy drift will not be enabled."
            self.errors_map["poor_meta_model"] = error_message
            logger.log_error(
                error_message,
                get_logging_params(
                    data_set=data_set,
                    start_time=start_time))
            return

        logger.log_info(
            f"Accuracy Drift Meta Model trained.",
            get_logging_params(
                data_set=data_set,
                start_time=start_time))

    def _fit_without_optimise(self, train_df, train_y_df):

        # Specifying that Probability Difference column has a monotonic constraint with the positive class.
        # Read https://scikit-learn.org/stable/modules/ensemble.html#monotonic-cst-gbdt
        monotonic_constraints = [0] * len(self.feature_columns)
        monotonic_constraints[self.feature_columns.index(META_MODEL_PROBABILITY_DIFF_COLUMN)] = 1

        initial_parameters = {
            "random_state": RANDOM_SEED,
            "learning_rate": 0.1,
            "verbose": 1,
            "monotonic_cst": monotonic_constraints
        }

        self.model_object = HistGradientBoostingClassifier(**initial_parameters)
        self.model_object.fit(train_df, train_y_df)

    def _check_accuracy(self, test_df):
        meta_model_predictions = self.model_object.predict(test_df)
        self.base_predicted_accuracy = sum(meta_model_predictions) / len(meta_model_predictions)
        threshold = ControlBoxManager().get_control_box().get_meta_model_base_accuracy_threshold()

        return abs(self.base_client_accuracy - self.base_predicted_accuracy) < threshold

    def predict_proba(self, data: pd.DataFrame) -> pd.Series:
        logger.log_info(f"Got dataframe of shape {data.shape} for scoring.")
        result_df = data.copy(deep=True)
        for feature in self.categorical_columns:
            # Unseen values in payload categorical columns are encoded as np.nan
            le = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=np.nan)
            le.fit(np.array(self.categorical_map[feature]).reshape(-1, 1))
            result_df = result_df.assign(
                **{feature: le.transform(result_df[feature].values.reshape(-1, 1))})

        # The top two highest probabilities
        sorted_probabilities = np.sort(result_df[self.probability_score_columns].values)[:, -2:]
        probability_difference = np.diff(sorted_probabilities).flatten()
        result_df = result_df.assign(**{META_MODEL_PROBABILITY_DIFF_COLUMN: probability_difference})

        probabilities = self.model_object.predict_proba(result_df[self.feature_columns])
        probabilities = pd.Series(probabilities[:, 0], index=result_df.index)
        return probabilities

    def to_dict(self) -> Dict:
        dict_ = super().to_dict()

        dict_["framework_version"] = str(sklearn.__version__)

        return dict_