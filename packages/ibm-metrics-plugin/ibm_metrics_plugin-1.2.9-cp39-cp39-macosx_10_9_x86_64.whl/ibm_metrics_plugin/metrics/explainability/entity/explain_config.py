# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# © Copyright IBM Corp. 2021, 2022  All Rights Reserved.
# US Government Users Restricted Rights -Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------

from ibm_metrics_plugin.common.utils.constants import InputDataType, ProblemType, ExplainabilityMetricType
from ibm_metrics_plugin.metrics.explainability.util.training_stats_reader import TrainingStatsReader


class ExplainConfig():
    """Explainability configuration containing the parameters required to generate explanation."""

    def __init__(self, input_data_type, problem_type, features, categorical_features=[], text_features=[], meta_fields=[], metric_types=[], prediction_column=None, probability_column=None, training_stats=None, training_data=None, features_schema={}, parameters={}, label_column=None, record_id_column=None, class_labels=None):
        """
        Arguments:
            input_data_type: 
                The type of input data. Possible values are "structured", "unstructured_text", "unstructured_image".
            problem_type: 
                The problem type. Possible values are "binary", "multiclass", "regression".
            features: 
                The list of features.
            categorical_features: 
                The list of categorical features.
            text_features: 
                The list of text features.
            meta_fields:
                The list of meta fields which needs to be sent while scoring.
            metrics:
                The list of metrics to compute.
            prediction_column:
                The prediction column name
            probability_column:
                The probability column name
            training_stats: 
                A dictionary having the details of training data statistics.
            training_data: 
                Training data pandas dataframe
            features_schema: 
                The datatypes of all the features as key value pairs
            parameters: 
                The configuration parameters specific to each explainer
            label_column:
                The label column name in training data
            record_id_column:
                The record id column name in the input data
        """
        self.input_data_type = input_data_type
        self.problem_type = problem_type
        self.features = features
        self.categorical_features = categorical_features
        self.text_features = text_features
        self.meta_fields = meta_fields
        cat_text = categorical_features + text_features
        self.numeric_features = [
            f for f in features if f not in cat_text]
        self.metric_types = metric_types
        self.prediction_column = prediction_column
        self.probability_column = probability_column
        self.training_data = training_data
        self.features_schema = features_schema
        self.parameters = parameters
        self.features_indexes = {k: v for v,
                                 k in enumerate(self.features)}
        self.label_column = label_column
        self.record_id_column = record_id_column
        self.class_labels = class_labels
        self.training_stats = training_stats
        self.scoring_fn = None

    @property
    def input_data_type(self):
        return self._input_data_type

    @input_data_type.setter
    def input_data_type(self, input_data_type):
        supported_types = [i.value for i in InputDataType]
        if input_data_type not in supported_types:
            raise ValueError("The input data type {0} is invalid. Valid types are {1}".format(
                input_data_type, supported_types))
        self._input_data_type = InputDataType(input_data_type)

    @property
    def problem_type(self):
        return self._problem_type

    @problem_type.setter
    def problem_type(self, problem_type):
        supported_types = [p.value for p in ProblemType]
        if problem_type not in supported_types:
            raise ValueError("The problem type {0} is invalid. Valid types are {1}".format(
                problem_type, supported_types))
        self._problem_type = ProblemType(problem_type)

    @property
    def features(self):
        return self._features

    @features.setter
    def features(self, features):
        if not (features and isinstance(features, list)):
            raise ValueError(
                "The features value {0} is invalid.".format(features))

        self._features = features

    @property
    def metric_types(self):
        return self._metric_types

    @metric_types.setter
    def metric_types(self, metric_types):
        supported_types = [e.value for e in ExplainabilityMetricType]
        if not all(t in supported_types for t in metric_types):
            raise ValueError("The metric types {0} are invalid. Valid types are {1}".format(
                metric_types, supported_types))

        self._metric_types = [
            ExplainabilityMetricType(e) for e in metric_types]

    @property
    def training_stats(self):
        return self._training_stats

    @training_stats.setter
    def training_stats(self, training_stats):
        if training_stats and self.input_data_type is InputDataType.STRUCTURED:
            stats_reader = TrainingStatsReader(training_stats=training_stats,
                                               features_schema=self.features_schema)
            self._training_stats = stats_reader.training_stats
        else:
            self._training_stats = None

    @staticmethod
    def load(config):
        conf = config.get("configuration")
        explainability = conf.get("explainability") or {}
        parameters = explainability.get("metrics_configuration")

        return ExplainConfig(input_data_type=conf.get("input_data_type"),
                             problem_type=conf.get("problem_type"),
                             features=conf.get("feature_columns"),
                             categorical_features=conf.get(
                                 "categorical_columns") or [],
                             meta_fields=conf.get("meta_columns") or [],
                             training_stats=explainability.get(
                                 "training_statistics"),
                             metric_types=list(parameters.keys()),
                             label_column=conf.get("label_column"),
                             prediction_column=conf.get("prediction"),
                             probability_column=conf.get("probability"),
                             record_id_column=conf.get("record_id"),
                             class_labels=conf.get("class_labels"),
                             features_schema=conf.get("features_schema", {}),
                             parameters=parameters)
