import logging
import os
import time
from domino import Domino

logger = logging.getLogger(__name__)

GENERIC_MODEL_FILE = "model.py"
GENERIC_MODEL_FUNCTION = "predict"


def _dm_api():
    return Domino(
        "{}/{}".format(
            os.getenv("DOMINO_PROJECT_OWNER"), os.getenv("DOMINO_PROJECT_NAME")
        )
    )


# published_model does not contain a version id
# use get_model_versions to select the version id or
# use active_status
def deploy_new_model(
    model_name,
    env_id,
    model_file=GENERIC_MODEL_FILE,
    model_function=GENERIC_MODEL_FUNCTION,
):
    dm_api = _dm_api()
    published_model = dm_api.model_publish(
        file=model_file,
        function=model_function,
        environment_id=env_id,
        name=model_name,
        description="Autopublish of MLFLOW model {}".format(model_name),
    )
    published_model_id = published_model.get("data", {}).get("_id")
    logger.debug("Model {} published, details below:".format(published_model_id))
    logger.debug(published_model)
    return published_model_id, get_latest_version_id(published_model_id)


# The API returns the following
# {'id': '63668cf7b6589d515ab59314', 'number': 6}
# and that entire JSON is returned to the caller
def deploy_new_version(
    published_model_id,
    env_id,
    model_file=GENERIC_MODEL_FILE,
    model_function=GENERIC_MODEL_FUNCTION,
):
    dm_api = _dm_api()
    another_model_version = dm_api.model_version_publish(
        model_id=published_model_id,
        file=model_file,
        function=model_function,
        environment_id=env_id,
        description="",
    )
    return another_model_version.get("id")


# Publish a new model or version as applicable
def deploy_model(project_id, model_name, env_id, wait_until_running):
    model_id = get_model_id(project_id, model_name)
    if model_id:
        stop_all_deployments(model_id)
        time.sleep(10)
        model_version_id = deploy_new_version(model_id, env_id)
    else:
        model_id, model_version_id = deploy_new_model(model_name, env_id)
    if wait_until_running:
        _wait_for_deployment(model_id, model_version_id)
    return model_id, model_version_id


# List_envs produces a list of objects containing the env id, name and visibility
# e.g. {'id': '63629f9823381b6c3b43ab39', 'name': 'CudaGpu', 'visibility': 'Private'}
# This list is obtained by selecting the attribute 'data' from the JSON returned by the API
# e.g. all_available_environments["data"] as used below
def list_envs():
    dm_api = _dm_api()
    all_available_environments = dm_api.environments_list()
    global_environments = list(
        filter(
            lambda x: x.get("visibility") == "Global",
            all_available_environments["data"],
        )
    )
    logger.debug(
        "This Domino deployment has \
       {} global environments".format(
            len(global_environments)
        )
    )
    # logger.debug(global_environments[0])
    return all_available_environments["data"]


# The API returns an array of 'data'
# {
#     "data": [
#         {
#             "_id": "63669299b6589d515ab5931e",
#             "modelId": {"value": "63652e0723381b6c3b43b0c1"},
#             "projectId": "62ab876f4353fd13a0e04f89",
#             "commitId": "7e831d4ed018b2c094408f874b3ecbe92baa1143",
#             "file": "model.py",
#             "function": "my_model",
#             "excludeFiles": [],
#             "environmentRevisionId": "633220ba38fe2d4f0087c92c",
#             "metadata": {
#                 "createdBy": "62ab876e030b0306f5095bcb",
#                 "created": 1667666585511,
#                 "number": 8,
#                 "summary": "v2",
#                 "builds": [
#                     {
#                         "buildId": {"value": "63669299d9a5656520219b0d"},
#                         "slug": {
#                             "image": {
#                                 "repository": "dominodatalab/model",
#                                 "tag": "63652e0723381b6c3b43b0c1-v8-202211516435_ghUsj1oA",
#                             }
#                         },
#                     }
#                 ],
#             },
#             "logHttpRequestResponse": False,
#             "recordInvocation": True,
#             "monitoringEnabled": False,
#         },
#       ...
#         {
#             "_id": "63652e0723381b6c3b43b0c3",
#             "modelId": {"value": "63652e0723381b6c3b43b0c1"},
#             "projectId": "62ab876f4353fd13a0e04f89",
#             "commitId": "6ee74a81818e0d16154ec074633ca621e8cf4c18",
#             "file": "model.py",
#             "function": "my_model",
#             "excludeFiles": [],
#             "environmentRevisionId": "633220ba38fe2d4f0087c92c",
#             "metadata": {
#                 "createdBy": "62ab876e030b0306f5095bcb",
#                 "created": 1667575303956,
#                 "number": 1,
#                 "builds": [
#                     {
#                         "buildId": {"value": "63652e08d9a5656520205cf1"},
#                         "slug": {
#                             "image": {
#                                 "repository": "dominodatalab/model",
#                                 "tag": "63652e0723381b6c3b43b0c1-v1-2022114152144_NW34uhEr",
#                             }
#                         },
#                     },
#                     {
#                         "buildId": {"value": "63652e08d9a5656520205cf1"},
#                         "slug": {
#                             "image": {
#                                 "repository": "dominodatalab/model",
#                                 "tag": "63652e0723381b6c3b43b0c1-v1-2022114152144_NW34uhEr",
#                             }
#                         },
#                     },
#                 ],
#             },
#             "logHttpRequestResponse": False,
#             "recordInvocation": True,
#             "monitoringEnabled": False,
#         }
#     ]
# }
# You can get the latest version from this array but not the status
# To wait for a new model version to start running you have to check_build_status
# and wait for status == 'complete', then use active_status to make sure that
# the versions match and that the status == 'Running'
def describe_model_versions(model_id):
    dm_api = _dm_api()
    model_versions = dm_api.model_versions_get(model_id)
    logger.debug(
        "Model {} \
        has {} versions:".format(
            model_id, len(model_versions.get("data", []))
        )
    )
    logger.debug(model_versions)
    logger.debug(model_versions.get("data", [])[0].get("_id"))
    logger.debug(model_versions.get("data", [])[0].get("metadata", {}).get("number"))
    return model_versions.get("data", [])


def get_latest_version_id(model_id):
    versions = describe_model_versions(model_id)
    return versions[0].get("_id", None)


# nv_pairs is a dictionary of name/value pairs, {'name': 'value'}
def add_env_vars(model_id, nv_pairs):
    dm_api = _dm_api()
    # request = {"vars": [{"name": "var6", "value": "var6"}]}
    vars_array = [
        {"name": str(name), "value": str(value)} for (name, value) in nv_pairs.items()
    ]
    request = {"vars": vars_array}
    api_host = os.getenv("DOMINO_API_HOST")
    resp = dm_api.request_manager.post(
        f"{api_host}/models/{model_id}/environmentVariables/add", json=request
    )
    logger.debug(resp.text)


def model_status(model_id):
    dm_api = _dm_api()
    api_host = os.getenv("DOMINO_API_HOST")
    resp = dm_api.request_manager.get(
        f"{api_host}/v4/modelManager/{model_id}/getModelReproductionDetails"
    )
    # First element is the latest version
    if resp and len(resp.json()) > 0:
        logger.debug(resp.json())
        return resp.json()[0].get("modelVersionId"), resp.json()[0].get("status")
    raise Exception(f"Model status for {model_id} returned an empty array")


# getBuildStatus API returns the following
# {'modelId': '63652e0723381b6c3b43b0c1', 'modelVersionId': '63668cf7b6589d515ab59314', 'status': 'complete'}
def build_status(model_id, model_version_id):
    dm_api = _dm_api()
    api_host = os.getenv("DOMINO_API_HOST")
    # resp = dm_api.request_manager.get(f'{api_host}/models/{model_id}/activeStatus',json={})
    resp = dm_api.request_manager.get(
        f"{api_host}/v4/models/{model_id}/{model_version_id}/getBuildStatus"
    )
    logger.debug(resp.json())
    return resp.json().get("status")


# activeStatus API returns the following
# {
#     "modelId": {"value": "63652e0723381b6c3b43b0c1"},
#     "modelVersionId": {"value": "6365532ab6589d515ab591ab"},
#     "status": "Failed",
#     "operations": [
#         {
#             "startTime": 1667584810609,
#             "endTime": 1667585078527,
#             "lastUpdated": 1667585078527,
#             "sagaDescription": "Deploy model version",
#             "shortStateDescription": "Deploy Failed",
#             "longStateDescription": "Build failed",
#             "isFailure": True,
#         },
#         {
#             "startTime": 1667593115289,
#             "endTime": 1667593154953,
#             "lastUpdated": 1667593154953,
#             "sagaDescription": "Stop model version",
#             "shortStateDescription": "Stopped",
#             "longStateDescription": "Model Version Stopped",
#             "isFailure": False,
#         },
#     ],
#     "isPending": False,
# }
# From this structure we select the model version id and the status
#
# Note: active_status only returns the active version or the last failed version of
# a deployed model. If you kick off a new deployment and it's still building, active_status
# will not reflect that version.
def active_status(model_id):
    dm_api = _dm_api()
    api_host = os.getenv("DOMINO_API_HOST")
    resp = dm_api.request_manager.get(
        f"{api_host}/models/{model_id}/activeStatus", json={}
    )
    logger.debug(resp.json())
    logger.debug(resp.json().get("modelId", {}).get("value", None))
    status = resp.json().get("status", "")
    model_version_id = resp.json().get("modelVersionId", {}).get("value", None)
    return model_version_id, status


def _wait_for_deployment(model_id, model_version_id):
    status = None
    while True:
        logger.debug(
            f"Checking status for model {model_id}, version {model_version_id}"
        )
        deploy_version_id, status = model_status(model_id)
        if deploy_version_id != model_version_id:
            raise Exception(
                f"Version being deployed {deploy_version_id} not the same as given version {model_version_id}"
            )
        if "running" == status.lower() or "failed" in status.lower():
            break
        time.sleep(20)
    if "failed" in status.lower():
        raise Exception(
            f"Model {model_id}, version {model_version_id} failed to deploy"
        )


# get_models returns a json array containing these attributes
# [{
#     "id": "63652e0723381b6c3b43b0c1",
#     "name": "my_model",
#     "description": "Autopublish of MLFLOW model my_model",
#     "activeVersionNumber": 5,
#     "activeModelVersionId": "6365532ab6589d515ab591ab",
#     "activeVersionStatus": "Failed",
#     "lastModified": 1667660815007,
#     "projectId": "62ab876f4353fd13a0e04f89",
#     "projectName": "quick-start",
#     "projectOwnerUsername": "first.last",
#     "owners": [{"id": "62ab876e030b0306f5095bcb", "name": "first.last"}],
# }]
def get_models(project_id):
    dm_api = _dm_api()
    api_host = os.getenv("DOMINO_API_HOST")
    resp = dm_api.request_manager.get(
        f"{api_host}/v4/modelManager/getModels?projectId={project_id}"
    )
    logger.debug(resp.status_code == 200)
    # logger.debug(resp.json()[0].get("name"))
    logger.debug(resp.json())
    # for j in resp.json():
    #    logger.debug(j.get('name'))
    return resp.json()


# Iterate through get_models to match name
def get_model_id(project_id, model_name):
    for j in get_models(project_id):
        if j.get("name", "") == model_name:
            return j.get("id")
    return None


# stopModelDeployment API returns the following
# {"modelId":"63652e0723381b6c3b43b0c1","modelVersionId":"63654db2b6589d515ab59184","status":"not_running"}
# status can be used to wait until 'not_running'
def stop_deployment(model_id, model_version_id):
    dm_api = _dm_api()
    api_host = os.getenv("DOMINO_API_HOST")
    resp = dm_api.request_manager.post(
        f"{api_host}/v4/models/{model_id}/{model_version_id}/stopModelDeployment"
    )
    logger.debug(resp.text)


# Iterate through describe_model_versions and use stop_deployment
def stop_all_deployments(model_id):
    for j in describe_model_versions(model_id):
        model_version_id = j.get("_id")
        vers_num = j.get("metadata", {}).get("number")
        logger.debug(
            "Stopping version number {}, version {}".format(vers_num, model_version_id)
        )
        stop_deployment(model_id, model_version_id)


# The API returns the following
# {
#     "id": "63651fb323381b6c3b43b0a3",
#     "projectId": "62ab876f4353fd13a0e04f89",
#     "number": 65,
#     "startingUserId": "62ab876e030b0306f5095bcb",
#     "queued": 1667571635060,
#     "started": 1667572078943,
#     "completed": None,
#     "status": "Running",
#     "commitId": "6ee74a81818e0d16154ec074633ca621e8cf4c18",
#     "startingScheduledRunId": None,
#     "outputCommitId": "7e831d4ed018b2c094408f874b3ecbe92baa1143",
#     "title": "CudaTest",
#     "publiclyVisible": False,
#     "isArchived": False,
#     "postProcessedTimestamp": None,
#     "diagnosticStatistics": None,
#     "isCompleted": False,
#     "hardwareTierId": "gpu-small-k8s",
#     "environmentId": "63629f9823381b6c3b43ab39",
#     "environmentRevisionId": "6362b38623381b6c3b43adf6",
#     "repositories": [],
#     "notebookName": "JupyterLab",
#     "runQueueingInformation": None,
#     "datasetMounts": [
#         {
#             "containerPath": "/domino/datasets/local/quick-start",
#             "datasetId": "62ab87704353fd13a0e04f8d",
#             "snapshotId": "62ab87704353fd13a0e04f8c",
#             "isReadOnly": False,
#             "resourceId": "23e286ab-8e07-4a6f-8ada-ff87445f577a",
#             "resourcePath": "23e286ab-8e07-4a6f-8ada-ff87445f577a",
#         }
#     ],
#     "containerExitCode": None,
#     "autoSyncSettings": None,
# }
# Use this to select environmentId or hardwareTierId
# e.g. run_inf.get('hardwareTierId')
#
# Invoke this using a Domino run id
# e.g. os.getenv("DOMINO_RUN_ID")
def run_info(domino_run_id):
    dm_api = _dm_api()
    run_inf = dm_api.get_run_info(domino_run_id)
    logger.debug(run_inf)
    return run_inf


# Iterate through list_envs and select on env_id
# Return the object containing th id, name and visibility
# e.g. {'id': '63629f9823381b6c3b43ab39', 'name': 'CudaGpu', 'visibility': 'Private'}
def env_info(env_id):
    for e in list_envs():
        if e.get("id") == env_id:
            logger.debug(e)
            return e
    return None


# list_envs()
# deploy_model('my_model',env_id='626079e621e807097859ee03')
# an_ver=publish_new_version('63652e0723381b6c3b43b0c1',env_id='626079e621e807097859ee03')
# print(f'\n\n\nPublished new version {an_ver}\n\n\n')
# describe_model_versions(model_id='63652e0723381b6c3b43b0c1')
# stop_deployment(model_id='63652e0723381b6c3b43b0c1',model_version_id='63654db2b6589d515ab59184')
# check_publish_status(model_id='63652e0723381b6c3b43b0c1',model_version_id='63654db2b6589d515ab59184')
# get_models('62ab876f4353fd13a0e04f89')
# add_env_vars(model_id='63652e0723381b6c3b43b0c1')
# active_status(model_id="63652e0723381b6c3b43b0c1")
# stop_all_deployments(model_id='63652e0723381b6c3b43b0c1')
# run_id = os.getenv("DOMINO_RUN_ID")
# run_inf = run_info(domino_run_id=run_id)
# print(run_inf.get("environmentId"))
# print(run_inf.get("hardwareTierId"))
# env_info("63629f9823381b6c3b43ab39")
