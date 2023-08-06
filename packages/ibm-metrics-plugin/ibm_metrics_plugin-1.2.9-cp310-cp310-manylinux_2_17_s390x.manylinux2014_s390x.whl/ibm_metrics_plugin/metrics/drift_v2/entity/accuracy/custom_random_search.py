# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2022
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

import sys

import tqdm
from ibm_metrics_plugin.common.utils.metrics_logger import MetricLogger
from ibm_metrics_plugin.metrics.drift_v2.utils.control_box import \
    ControlBoxManager
from sklearn.model_selection import ParameterSampler, RandomizedSearchCV

logger = MetricLogger(__name__)


class CustomRandomSearch(RandomizedSearchCV):
    _required_parameters = ["estimator", "param_distributions"]

    def __init__(
            self,
            estimator,
            param_distributions,
            progress_bar=True,
            callback=None,
            n_iter=10,
            scoring=None,
            n_jobs=None,
            refit=True,
            cv="warn",
            verbose=0,
            pre_dispatch="2*n_jobs",
            random_state=None,
            error_score="raise",
            return_train_score=False,
            model_stage=None):
        self.param_distributions = param_distributions
        self.n_iter = n_iter
        self.random_state = random_state
        self.progress_bar = progress_bar
        self.callback = callback
        self.model_stage = model_stage
        super().__init__(
            estimator=estimator, param_distributions=self.param_distributions,
            n_iter=self.n_iter, random_state=self.random_state,
            scoring=scoring,
            n_jobs=n_jobs, refit=refit, cv=cv, verbose=verbose,
            pre_dispatch=pre_dispatch, error_score=error_score,
            return_train_score=return_train_score)

    def _run_search(self, evaluate_candidates):
        """Search n_iter candidates from param_distributions"""
        params = list(ParameterSampler(self.param_distributions,
                                       self.n_iter, random_state=self.random_state))

        tqdm_bar = tqdm(
            total=len(params),
            desc="Optimising Meta Model...",
            file=sys.stdout,
            unit="models",
            dynamic_ncols=True,
            disable=not(
                ControlBoxManager().get_control_box().get_show_progress_bar()))
        for idx, param in enumerate(params):
            evaluate_candidates([param])
            logger.log_info(f"Optimising meta model {idx}/{len(params)}.")
            tqdm_bar.update()
        tqdm_bar.close()
