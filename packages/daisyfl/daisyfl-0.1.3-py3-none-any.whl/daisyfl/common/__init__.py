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
"""Flower utilities shared between server and client."""


from .parameter import bytes_to_ndarray as bytes_to_ndarray
from .parameter import ndarray_to_bytes as ndarray_to_bytes
from .parameter import ndarrays_to_parameters as ndarrays_to_parameters
from .parameter import parameters_to_ndarrays as parameters_to_ndarrays
from .parameter import encode_ndarrays as encode_ndarrays
from .parameter import decode_ndarrays as decode_ndarrays
from .typing import Code as Code
from .typing import DisconnectRes as DisconnectRes
from .typing import EvaluateIns as EvaluateIns
from .typing import EvaluateRes as EvaluateRes
from .typing import FitIns as FitIns
from .typing import FitRes as FitRes
from .typing import GetParametersIns as GetParametersIns
from .typing import GetParametersRes as GetParametersRes
from .typing import GetPropertiesIns as GetPropertiesIns
from .typing import GetPropertiesRes as GetPropertiesRes
from .typing import Metrics as Metrics
from .typing import MetricsAggregationFn as MetricsAggregationFn
from .typing import NDArray as NDArray
from .typing import NDArrays as NDArrays
from .typing import Parameters as Parameters
from .typing import Properties as Properties
from .typing import ReconnectIns as ReconnectIns
from .typing import Scalar as Scalar
from .typing import Element as Element
from .typing import Status as Status
from .typing import Task as Task
from .typing import Report as Report
from .typing import Type as Type
from .typing import MetaTask as MetaTask


GRPC_MAX_MESSAGE_LENGTH: int = 536_870_912  # == 512 * 1024 * 1024
PIDS = "pids/"
NUM_ROUNDS = "NUM_ROUNDS"
CURRENT_ROUND = "CURRENT_ROUND"
EVALUATE = "EVALUATE"
TIMEOUT = "TIMEOUT"
FIT_SAMPLES = "FIT_SAMPLES"
EVALUATE_SAMPLES = "EVALUATE_SAMPLES"
LOSS = "LOSS"
METRICS = "METRICS"
TID = "TID"
OPERATION_PATH = "OPERATION_PATH"
OPERATION_SERVER = "OPERATION_SERVER"
OPERATION_ZONE_CLIENT = "OPERATION_ZONE_CLIENT"
OPERATION_ZONE_SERVER = "OPERATION_ZONE_SERVER"
OPERATION_CLIENT = "OPERATION_CLIENT"
STRATEGY_PATH = "STRATEGY_PATH"
STRATEGY = "STRATEGY"
LOAD_OPERATION = "LOAD_OPERATION"
# will be deprecated
USER_DEFINED_PLUGIN = "USER_DEFINED_PLUGIN"
ZONE_CLIENT_PLUGIN = "ZONE_CLIENT_PLUGIN"
USER_DEFINED_PLUGIN = "USER_DEFINED_PLUGIN"

__all__ = [
    "OPERATION_PATH",
    "OPERATION_SERVER",
    "OPERATION_ZONE_CLIENT",
    "OPERATION_ZONE_SERVER",
    "OPERATION_CLIENT",
    "STRATEGY_PATH"
    "STRATEGY",
    "LOAD_OPERATION",
    "PIDS",
    "NUM_ROUNDS",
    "CURRENT_ROUND",
    "EVALUATE",
    "TIMEOUT",
    "FIT_SAMPLES",
    "EVALUATE_SAMPLES",
    "LOSS",
    "METRICS",
    "Type",
    "MetaTask",
    "encode_ndarrays",
    "decode_ndarrays",
    "bytes_to_ndarray",
    "Code",
    "Element",
    "DisconnectRes",
    "EvaluateIns",
    "EvaluateRes",
    "FitIns",
    "FitRes",
    "GetParametersIns",
    "GetParametersRes",
    "GetPropertiesIns",
    "GetPropertiesRes",
    "GRPC_MAX_MESSAGE_LENGTH",
    "Metrics",
    "MetricsAggregationFn",
    "ndarray_to_bytes",
    "NDArray",
    "NDArrays",
    "ndarrays_to_parameters",
    "Parameters",
    "parameters_to_ndarrays",
    "Properties",
    "ReconnectIns",
    "Scalar",
    "Status",
    "Task",
    "Report",
    "TID",
    "USER_DEFINED_PLUGIN",
    "ZONE_CLIENT_PLUGIN",
    "USER_DEFINED_PLUGIN",
]
