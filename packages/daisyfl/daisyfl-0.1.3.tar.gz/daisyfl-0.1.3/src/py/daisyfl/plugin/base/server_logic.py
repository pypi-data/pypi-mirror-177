# Copyright 2020 Adap GmbH. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
from logging import INFO, WARNING
from typing import Dict, List, Optional, Tuple, TypedDict
from daisyfl.server import Server as BaseServer
from daisyfl.server.client_manager import ClientManager
from daisyfl.server.strategy import Strategy
from daisyfl.common import (
    FitIns,
    FitRes,
    Parameters,
    Scalar,
    Report,
    Task,
    CURRENT_ROUND,
    TIMEOUT,
    FIT_SAMPLES,
    METRICS,
    parameters_to_ndarrays,
    ndarrays_to_parameters,
    NDArrays,
)

from daisyfl.server.client_proxy import ClientProxy

from daisyfl.common.logger import log

FitResultsAndFailures = Tuple[List[Tuple[ClientProxy, FitRes]], List[BaseException]]

class Server(BaseServer):
    """Wrapper which adds SecAgg methods."""

    def __init__(
        self,
        s: BaseServer,
    ) -> None:
        self.server = s

    def disconnect_all_clients(self, timeout: Optional[float]) -> None:
        """Send shutdown signal to all clients."""
        self.server.disconnect_all_clients(timeout)

    def fit_round(
        self,
        parameters: Parameters,
        task: Task,
    ) -> Optional[
        Tuple[Optional[Parameters], Optional[Report]]
    ]:
        """Perform a single round fit."""
        # Get clients and their respective instructions from strategy
        client_instructions = self.server.get_configure_fit(
            server_round=task.config[CURRENT_ROUND],
            parameters=parameters,
            client_manager=self.server.get_client_manager(),
            config=task.config,
        )
        # Collect `fit` results from all clients participating in this round
        results, failures = self.server.fit_clients(
            client_instructions=client_instructions,
            max_workers=self.server.get_max_workers(),
            timeout=task.config[TIMEOUT],
        )
        # Aggregate training results
        parameters_aggregated, samples, metrics_aggregated  = self.server.aggregate_fit(
            task.config[CURRENT_ROUND],
            results,
            failures,
        )
        # Get report
        report = self.server.generate_fit_report(
            task.config[CURRENT_ROUND],
            samples,
            metrics_aggregated,
        )

        return parameters_aggregated, report

    def evaluate_round(
        self, 
        parameters: Parameters,
        task: Task,
    ) -> Optional[Report]:
        """Validate current global model on a number of clients."""
        # Get clients and their respective instructions from strategy
        client_instructions = self.server.get_configure_evaluate(
            server_round=task.config[CURRENT_ROUND],
            parameters=parameters,
            client_manager=self.server.get_client_manager(),
            config=task.config,
        )
        # Collect `evaluate` results from all clients participating in this round
        results, failures = self.server.evaluate_clients(
            client_instructions,
            max_workers=self.server.get_max_workers(),
            timeout=task.config[TIMEOUT],
        )
        # Aggregate the evaluation results
        loss_aggregated, samples, metrics_aggregated = self.server.aggregate_evaluate(
            task.config[CURRENT_ROUND],
            results,
            failures,
        )
        # Get report
        report = self.server.generate_evaluate_report(
            task.config[CURRENT_ROUND],
            samples,
            loss_aggregated,
            metrics_aggregated,
        )

        return report