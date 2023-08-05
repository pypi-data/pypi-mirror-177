import os
import jwt
from urllib.parse import urlparse
import mlflow
import domino_mlflow_client.tag_constants as constants
import domino_mlflow_client.model_utils as mdut

MODEL_ENV_VAR_ADD_URL = (
    "https://frbny.domino.tech/models/63652e0723381b6c3b43b0c1/environmentVariables/add"
)
MODEL_ENV_VARS_BODY = {"vars": [{"name": "var2", "value": "var2"}]}
MODEL_DEPLOYMENT_STATUS_URL = (
    "https://frbny.domino.tech/models/63652e0723381b6c3b43b0c1/activeStatus"
)


class DominoMLFlowClient:
    @staticmethod
    def init(
        mlflow_tracking_uri=None,
        domino_api_key=None,
        domino_project_name=None,
        domino_run_id=None,
        tags={},
    ):
        if mlflow_tracking_uri is not None:
            os.environ["MLFLOW_TRACKING_URI"] = mlflow_tracking_uri
        if domino_api_key is None:
            domino_api_key = os.environ.get("DOMINO_USER_API_KEY")
        if domino_project_name is None:
            domino_project_name = os.environ.get("DOMINO_PROJECT_NAME")
        if domino_run_id is None:
            domino_run_id = os.environ.get("DOMINO_RUN_ID")

        encoded_jwt = DominoMLFlowClient.generate_mlflow_token(
            domino_api_key, domino_project_name, domino_run_id, tags
        )
        os.environ["MLFLOW_TRACKING_TOKEN"] = encoded_jwt
        return encoded_jwt

    @staticmethod
    def generate_mlflow_token(
        domino_api_key=None, domino_project_name=None, domino_run_id=None, tags={}
    ):
        domino_json = {
            "domino_api_key": domino_api_key,
            "domino_project_name": domino_project_name,
            "domino_run_id": domino_run_id,
            "tags": tags,
        }
        encoded_jwt = jwt.encode(domino_json, "secret", algorithm="HS256")
        return encoded_jwt

    @staticmethod
    def update_tags(tags={}):
        domino_attributes = DominoMLFlowClient.decode_jwt(
            os.environ["MLFLOW_TRACKING_TOKEN"]
        )
        return DominoMLFlowClient.init(
            domino_attributes["domino_api_key"],
            domino_attributes["domino_project_name"],
            domino_attributes["domino_run_id"],
            tags,
        )

    @staticmethod
    def decode_jwt(encoded_jwt=None):
        return jwt.decode(encoded_jwt.encode(), "secret", algorithms=["HS256"])

    @staticmethod
    def deploy_domino_model_api_to_staging(
        mlflow_model_name, mlflow_model_version, env_id, wait_until_running=True
    ):

        mlflow_run_id, project_id, mlflow_model_owner = _get_model_domino_ids(
            mlflow_model_name,
            mlflow_model_version,
        )
        if not mlflow_run_id:
            raise Exception("Model does not have an associated run Id")
        if not project_id:
            raise Exception("Model does not have an associated project Id")
        if not env_id:
            raise Exception(
                "Need to provide an environment id that has mlflow and other packages required for the model"
            )

        if not _check_project_id_and_owner(project_id, mlflow_model_owner):
            raise Exception(
                "User cannot deploy model for a project other than the current one"
            )
        domino_model_id, domino_model_version_id = mdut.deploy_model(
            project_id, mlflow_model_name, env_id, wait_until_running
        )
        env_vars = {}
        env_vars["MLFLOW_MODEL_OWNER"] = mlflow_model_owner
        env_vars["MLFLOW_RUN_ID"] = mlflow_run_id
        env_vars["MLFLOW_MODEL_NAME"] = mlflow_model_name
        env_vars["MLFLOW_MODEL_VERSION"] = mlflow_model_version
        mdut.add_env_vars(domino_model_id, env_vars)

        mlflow_tags = {}
        mlflow_tags["DOMINO_MODEL_ID"] = domino_model_id
        mlflow_tags["DOMINO_MODEL_VERSION_ID"] = domino_model_version_id
        _update_mlflow_model_tags(mlflow_model_name, mlflow_model_version, mlflow_tags)

        _transition_mlflow_model_to_staging(mlflow_model_name, mlflow_model_version)


def _transition_mlflow_model_to_staging(model_name, model_version):
    client = mlflow.tracking.MlflowClient()
    # stage value is case sensitive
    client.transition_model_version_stage(
        str(model_name), str(model_version), stage="Staging"
    )


def _update_mlflow_model_tags(model_name, model_version, tags):
    client = mlflow.tracking.MlflowClient()
    for (key, value) in tags.items():
        client.set_model_version_tag(
            str(model_name), str(model_version), str(key), str(value)
        )


def _get_model_domino_ids(model_name, model_version):
    client = mlflow.tracking.MlflowClient()
    mv = client.get_model_version(model_name, model_version)
    if not mv:
        raise Exception(
            f"Model not registered for {model_name} with version {model_version}"
        )
    return (
        mv.run_id,
        mv.tags.get(constants.TAG_MLFLOW_DOMINO_PROJECT_ID, None),
        mv.tags.get(constants.TAG_MLFLOW_DOMINO_USER, None),
    )


def _check_project_id_and_owner(project_id, mlflow_model_owner):
    domino_project_id = os.getenv("DOMINO_PROJECT_ID")
    domino_user = os.getenv("DOMINO_STARTING_USERNAME")
    return domino_project_id == project_id and domino_user == mlflow_model_owner


# Testings
if __name__ == "__main__":
    from domino_mlflow_client import DominoMLFlowClient as dmc

    domino_api_key = "1"
    domino_project_name = "2"
    domino_runid = "3"
    domino_project_id = "4"
    key = dmc.init(
        "x",
        domino_api_key,
        domino_project_name,
        domino_runid,
        tags={"a": "b"},
    )
    print("---")
    print(key)
    print("---")
    print(dmc.decode_jwt(key))
