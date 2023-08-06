import secrets
from kubernetes import client, config
from kubernetes.client.models.v1_secret import V1Secret
from domino_mlflow_client import DominoMLFlowClient as dmc
import domino_mlflow_client.tag_constants as constants
import os


class ServiceAccountClient:
    @staticmethod
    def generate_service_account(
        domino_project_id, domino_project_name, domino_project_owner, tags={}
    ):
        tags[constants.TAG_DOMINO_HARDWARE_TIER_ID] = os.getenv(
            "DOMINO_HARDWARE_TIER_ID", ""
        )
        tags[constants.TAG_DOMINO_PROJECT_OWNER] = os.getenv("DOMINO_PROJECT_OWNER", "")
        tags[constants.TAG_DOMINO_PROJECT_OWNER] = domino_project_owner
        tags[constants.TAG_DOMINO_PROJECT_ID] = domino_project_id
        tags[constants.TAG_IS_SERVICE_ACCOUNT] = True
        domino_run_id = None
        encoded_jwt = dmc.generate_mlflow_token(
            secrets.token_urlsafe(64), domino_project_name, domino_run_id, tags
        )
        return encoded_jwt

    @staticmethod
    def save_mlflow_service_account(
        domino_project_id,
        mlflow_api_token,
        k8s_namespace,
        k8s_secret_name="mlflow-model-secret",
    ):
        try:
            config.load_incluster_config()
        except:
            print("Loading local k8s config")
            config.load_kube_config()
        v1 = client.CoreV1Api()
        secrets_body: V1Secret = v1.read_namespaced_secret(
            k8s_secret_name, k8s_namespace
        )
        if secrets_body.string_data == None:
            secrets_body.string_data = {}
        secrets_body.string_data[f"{domino_project_id}.apikey"] = mlflow_api_token
        v1.patch_namespaced_secret(k8s_secret_name, k8s_namespace, secrets_body)
        print(mlflow_api_token)
        # print(v1.read_namespaced_secret(k8s_secret_name, k8s_namespace))


if __name__ == "__main__":
    """
    svc_jwt = ServiceAccountClient.generate_service_account(
        "636bdd261e7a0803c73ad405", "mlops-demo", "srinivap"
    )
    ServiceAccountClient.save_mlflow_service_account(
        "636bdd261e7a0803c73ad405", svc_jwt, "mlflow-efs"
    )
    """
    import argparse

    parser = argparse.ArgumentParser(description="Generate mlflow service token")
    parser.add_argument("-i", "--domino-project-id", required=True)
    parser.add_argument("-n", "--domino-project-name", required=True)
    parser.add_argument("-o", "--domino-project-owner", required=True)
    parser.add_argument("-o", "--domino-mlflow-ns", required=True)
    parser.add_argument(
        "-s", "--secret-name", required=False, default="mlflow-proxy-secret"
    )

    args = parser.parse_args()

    project_id = args.domino_project_id
    project_name = args.domino_project_name
    project_owner = args.domino_project_owner
    mlflow_ns = args.domino_mlflow_ns
    secret_name = args.secret_name
    print(
        f"Creating Service Account Token for project_id={project_id},"
        f"project_name={project_name},project_owner={project_owner}, secret_name={secret_name}"
    )
    svc_jwt = ServiceAccountClient.generate_service_account(
        project_id, project_name, project_owner
    )
    # print(svc_jwt)
    ServiceAccountClient.save_mlflow_service_account(project_id, svc_jwt, mlflow_ns,secret_name)
    # ServiceAccountClient.save_mlflow_service_account("636bdd261e7a0803c73ad405",svc_jwt,"mlflow-efs")
