import os

import stochasticx
from stochasticx.utils.preferences import Preferences, AppModes

LOGIN_URL = stochasticx.BASE_URI + "/v1/auth/login"
MODELS_URL = stochasticx.BASE_URI + "/v1/models"
OPTIMIZED_MODELS_URL = stochasticx.BASE_URI + "/v1/processedModels"
REQUEST_UPLOAD_URL = stochasticx.BASE_URI + "/v1/upload/requestUpload"
MODEL_UPLOAD_URL = stochasticx.BASE_URI + "/v1/upload/model"
DATASET_UPLOAD_URL = stochasticx.BASE_URI + "/v1/upload/dataset"
DATASETS_URL = stochasticx.BASE_URI + "/v1/datasets"
ME_URL = stochasticx.BASE_URI + "/v1/auth/me"
JOBS_URL = stochasticx.BASE_URI + "/v1/jobs"
INSTANCES_URL = stochasticx.BASE_URI + "/v1/instances"
DEPLOYMENT_URL = stochasticx.BASE_URI + "/v1/deploy"
STABLE_DIFFUSION_URL = stochasticx.BASE_URI + "/v1/stdDeploy"

TOKEN_AUTH_PATH = os.path.expandvars("$HOME/.stochastic/token.json")
PREFERENCES_PATH = os.path.expandvars("$HOME/.stochastic/preferences.json")

INFERENCE_URL = stochasticx.BASE_URI + "http://infer.stochastic.ai:8000/"
FINETUNING_GET_JOBS_CLOUD_URL = stochasticx.BASE_URI + "/v1/finetuningJobs"


class CloudRoutes:
    LOGIN_URL = "/v1/auth/login"
    MODELS_URL = "/v1/models"
    OPTIMIZED_MODELS_URL = "/v1/processedModels"
    REQUEST_UPLOAD_URL = "/v1/upload/requestUpload"
    MODEL_UPLOAD_URL = "/v1/upload/model"
    DATASET_UPLOAD_URL = "/v1/upload/dataset"
    DATASETS_URL = "/v1/datasets"
    ME_URL = "/v1/auth/me"
    JOBS_URL = "/v1/jobs"
    INSTANCES_URL = "/v1/instances"
    DEPLOYMENT_URL = "/v1/deploy"
    INFERENCE_URL = "http://infer.stochastic.ai:8000/"


class LocalRoutes:
    HEALTH_REGISTRY = "http://127.0.0.1:3000/"
    LOGIN_URL = "/v1/auth/login"
    MODEL_URL = "/local/model"
    MODEL_UPLOAD_URL = "/local/model/upload"
    DATASET_URL = "/local/dataset"
    DATASET_UPLOAD_URL = "/local/dataset/upload"
    BENCHMARKING_URL = "http://localhost:5001/post_benchmarking_task"
    ONNX_CONVERSION_URL = "http://localhost:5000/onnx_conversion/"
    TENSORRT_CONVERSION_URL = "http://localhost:5000/tensorrt_conversion/"
    ONNX_INT8_CONVERSION_URL = "http://localhost:5000/onnx_conversion_int8/"

class CommonRoutes:
    LOGIN_URL = "LOGIN_URL"
    MODELS_URL = "MODELS_URL"






def get_cloud_url(suffix: str) -> str:
    # Read saved preferences
    preferences = Preferences.load()
    return preferences.cloud_url + suffix


def get_local_url(suffix: str) -> str:
    # Read saved preferences
    preferences = Preferences.load()
    return preferences.local_url + suffix


def get_common_url(suffix: str) -> str:
    # Read saved preferences
    print("Suffix: ", suffix)
    preferences = Preferences.load()
    current_mode = preferences.current_mode

    if current_mode == AppModes.CLOUD:
        return preferences.cloud_url + suffix 
    else:
        return preferences.local_url + suffix



# def test():

#     common_url = get_common_url(CommonRoutes.LOGIN_URL)

#     print("CommonURL: ", common_url)

#     cloud_url = get_cloud_url(CommonRoutes.LOGIN_URL)

#     print("CloudURL: ", cloud_url)

#     local_url = get_local_url(CommonRoutes.LOGIN_URL)

#     print("LocalURL: ", local_url)

# test()