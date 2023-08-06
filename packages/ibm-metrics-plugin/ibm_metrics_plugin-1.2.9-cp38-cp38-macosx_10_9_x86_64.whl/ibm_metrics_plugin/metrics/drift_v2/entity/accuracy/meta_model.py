# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2022
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

import pickle
from abc import abstractmethod
from typing import Dict

import numpy as np
import pandas as pd
from ibm_metrics_plugin.common.utils.python_utils import get_python_types
from ibm_metrics_plugin.metrics.drift_v2.entity.dataset.data_set import \
    DriftDataSet
from ibm_metrics_plugin.metrics.drift_v2.utils.constants import (
    META_MODEL_SANDBOX_CLASSES, META_MODEL_SANDBOX_MODULES, MetaModelKind)


class MetaModel:

    def __init__(self, kind: MetaModelKind) -> None:
        self.kind = kind
        self.feature_columns = []
        self.categorical_columns = []
        self.probability_score_columns = []
        self.probability_column = None
        self.is_balanced_data = False
        self.is_optimised = False
        self.categorical_map = {}
        self.errors_map = {}
        self.model_object = None
        self.base_client_accuracy = None
        self.base_predicted_accuracy = None

    @classmethod
    def factory(self,
                data: pd.DataFrame,
                data_set: DriftDataSet) -> "MetaModel":
        if isinstance(data, pd.DataFrame):
            # from ibm_metrics_plugin.metrics.drift_v2.entity.accuracy.sklearn_gbt_model import \
            #     GBTMetaModel
            # model = GBTMetaModel()
            from ibm_metrics_plugin.metrics.drift_v2.entity.accuracy.sklearn_hgbt_model import HGBTMetaModel
            model = HGBTMetaModel()
            model.fit(data, data_set)
            return model

    @abstractmethod
    def fit(self, data: pd.DataFrame, data_set: DriftDataSet) -> None:
        pass

    @abstractmethod
    def predict(self, data) -> None:
        pass

    @abstractmethod
    def predict_proba(self, data) -> np.ndarray:
        pass

    def load(self, model_object: object):
        self.model_object = RestrictedUnpickler(model_object).load()

    def to_dict(self) -> Dict:

        dict_ = {
            "kind": self.kind.value,
            "feature_columns": self.feature_columns,
            "categorical_columns": self.categorical_columns,
            "probability_column": self.probability_column,
            "probability_score_columns": self.probability_score_columns,
            "base_client_accuracy": get_python_types(self.base_client_accuracy),
            "base_predicted_accuracy": get_python_types(self.base_predicted_accuracy),
            "categorical_map": get_python_types(self.categorical_map),
            "errors_map": self.errors_map,
            "is_balanced_data": self.is_balanced_data,
            "is_optimised": self.is_optimised
        }

        return dict_

    @classmethod
    def from_dict(cls, dict_: Dict) -> "MetaModel":
        from ibm_metrics_plugin.metrics.drift_v2.entity.accuracy.sklearn_gbt_model import \
            GBTMetaModel
        from ibm_metrics_plugin.metrics.drift_v2.entity.accuracy.sklearn_hgbt_model import HGBTMetaModel

        try:
            model = None
            mm_kind = MetaModelKind(dict_["kind"])
            if mm_kind == MetaModelKind.SKLEARN_GBT:
                model = GBTMetaModel()
            elif mm_kind == MetaModelKind.SKLEARN_HGBT:
                model = HGBTMetaModel()

            model.feature_columns = dict_["feature_columns"]
            model.categorical_columns = dict_["categorical_columns"]
            model.probability_column = dict_["probability_column"]
            model.probability_score_columns = dict_["probability_score_columns"]
            model.base_client_accuracy = dict_["base_client_accuracy"]
            model.base_predicted_accuracy = dict_["base_predicted_accuracy"]
            model.is_balanced_data = dict_["is_balanced_data"]
            model.is_optimised = dict_["is_optimised"]
            model.categorical_map = dict_["categorical_map"]
            return model
        except KeyError as e:
            raise ValueError(
                f"Cannot create the meta model from the given dictionary. Missing key {e}.") from e


class RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        # Only allow safe classes from sandbox.
        if (module in META_MODEL_SANDBOX_MODULES) and (name in META_MODEL_SANDBOX_CLASSES):
            return super(RestrictedUnpickler, self).find_class(module, name)
        # Forbid everything else.
        raise pickle.UnpicklingError(f"'{module}.{name}' is forbidden to load.")
