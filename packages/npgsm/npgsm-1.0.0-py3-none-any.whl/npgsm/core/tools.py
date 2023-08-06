import hashlib
import json
import logging
import os
from typing import Optional

import google.cloud.logging
from google.api_core import exceptions
from google.api_core.retry import Retry, if_exception_type
from google.cloud import secretmanager

_MY_RETRIABLE_TYPES = (
    exceptions.TooManyRequests,  # 429
    exceptions.InternalServerError,  # 500
    exceptions.BadGateway,  # 502
    exceptions.ServiceUnavailable,  # 503
)


class NPGSM(object):
    def __init__(self, project_id, gcp_service_account_path: Optional[str] = None):
        self.project_id = project_id
        self.path_json_key = gcp_service_account_path
        self.__add_environment()
        self.client = self.__get_client()

    def __add_environment(self):
        if self.path_json_key:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.path_json_key

    def __get_client(self):
        client = google.cloud.logging.Client(project=self.project_id)
        client.setup_logging(log_level=logging.INFO)
        return secretmanager.SecretManagerServiceClient()

    # ================================= Utility functions =================================
    def create_secret(self, secret_id):
        # Example input: create_secret("my_secret_value")
        # Create the Secret Manager client.
        # Build the resource name of the parent project.
        parent = f"projects/{self.project_id}"
        # Build a dict of settings for the secret
        secret = {"replication": {"automatic": {}}}
        # Create the secret
        response = self.client.create_secret(
            secret_id=secret_id, parent=parent, secret=secret  # type: ignore
        )
        # Print the new secret name.
        print(f"Created secret: {response.name}")

    def add_secret_version(self, secret_id, payload):
        # add_secret_version("my_secret_value", "Hello Secret Manager")
        # add_secret_version("my_secret_value", "Hello Again, Secret Manager")
        # Create the Secret Manager client.
        client = secretmanager.SecretManagerServiceClient()
        # Build the resource name of the parent secret.
        parent = f"projects/{self.project_id}/secrets/{secret_id}"
        # Convert the string payload into a bytes. This step can be omitted if you
        # pass in bytes instead of a str for the payload argument.
        if isinstance(payload, str):
            payload = payload.encode("utf-8")
        elif isinstance(payload, dict):
            payload = json.dumps(payload).encode("utf-8")
        # Add the secret version.
        response = client.add_secret_version(parent=parent, payload={"data": payload})  # type: ignore
        # Print the new secret version name.
        print(f"Added secret version: {response.name}")

    def access_secret_version(self, secret_id, version_id="latest"):
        # view the secret value
        # Create the Secret Manager client.
        client = secretmanager.SecretManagerServiceClient()
        # Build the resource name of the secret version.
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version_id}"
        # Access the secret version.
        response = client.access_secret_version(name=name)
        # Return the decoded payload.
        payload = response.payload.data.decode("UTF-8")  # type: ignore
        return payload

    # def secret_hash(secret_value):
    #     # return the sha224 hash of the secret value
    #     return hashlib.sha224(bytes(secret_value, "utf-8")).hexdigest()
