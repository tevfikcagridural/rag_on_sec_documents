# Resource: https://blog.gitguardian.com/how-to-handle-secrets-with-google-cloud-secret-manager/

from google.cloud import secretmanager
import google_crc32c


def get_secret(secret_id: str, project_num: str="530660057944", version_id: str="latest") -> str:

    client = secretmanager.SecretManagerServiceClient()

    name = f"projects/{project_num}/secrets/{secret_id}/versions/{version_id}"

    response = client.access_secret_version(request={"name": name})

    # verify payload cheksum
    crc32c = google_crc32c.Checksum()
    crc32c.update(response.payload.data)
    if response.payload.data_crc32c != int(crc32c.hexdigest(), 16):
        print(f"Data corruption detected for {secret_id} !")
        
    secret = response.payload.data.decode("UTF-8")
    return secret