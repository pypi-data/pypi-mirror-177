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
import numpy as np
from typing import Dict, List, Tuple, TypedDict
from daisyfl.common import (
    ndarrays_to_parameters,
    parameters_to_ndarrays,
    Status,
    Code,
    FitIns,
    FitRes,
    GetParametersIns,
    GetParametersRes,
    GetPropertiesIns,
    GetPropertiesRes,
    EvaluateIns,
    EvaluateRes,
    NDArrays,
)
from daisyfl.common.logger import log
from logging import DEBUG, ERROR, INFO, WARNING
from daisyfl.client import Client as BaseClient

class Client(BaseClient):
    """Wrapper which adds SecAgg methods."""
    
    def __init__(self, c: BaseClient) -> None:
        self.client = c
    
    def get_parameters(self, ins: GetParametersIns) -> GetParametersRes:
        """Return the current local model parameters."""
        return self.client.get_parameters(ins)
    
    def get_properties(self, ins: GetPropertiesIns) -> GetPropertiesRes:
        """Return set of client's properties."""
        return self.client.get_properties(ins)
    
    def fit(
        self, ins: FitIns,
    ) -> FitRes:
        return self.client.fit(ins)

    def evaluate(
        self, ins: EvaluateIns,
    ) -> EvaluateRes:
        return self.client.evaluate(ins)