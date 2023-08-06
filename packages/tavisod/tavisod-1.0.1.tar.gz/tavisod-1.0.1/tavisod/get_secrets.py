# Import the Secret Manager client library.
from google.cloud import secretmanager
import os

class getSecret(object):
    def __init__(self, secret_id) -> str:
        if os.getenv(secret_id):
            return os.getenv(secret_id) 
        # Create the Secret Manager client.
        client = secretmanager.SecretManagerServiceClient()
        # Build the resource name of the secret version.
        name = f"projects/{os.getenv('PROJECT_ID')}/secrets/{secret_id}/versions/latest"
        # Access the secret version.
        response = client.access_secret_version(name=name)
        return response
