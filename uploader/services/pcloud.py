import requests
from django.conf import settings

API_PCLOUD_URL = settings.API_PCLOUD_URL
ACCESS_TOKEN = settings.PCLOUD_TOKEN

# chemin complet vers TON dossier TO_POST
TO_POST_PATH = "/Montage-EVENT/ALL_MONTAGE/RENDU_MONTAGE-COURT/TO_POST"


def upload_to_pcloud(file_obj, new_filename: str) -> str:
    """
    Upload la vidéo dans le dossier TO_POST (via path) et retourne le fileid.
    """
    url = f"{API_PCLOUD_URL}/uploadfile"

    params = {
        "access_token": ACCESS_TOKEN,
        "path": TO_POST_PATH,   # <-- plus de folderid ici
    }

    files = {
        "file": (new_filename, file_obj.read(), "video/mp4")
    }

    response = requests.post(url, params=params, files=files)
    data = response.json()

    print("DEBUG_PCLOUD_UPLOAD:", url, params, data)

    if data.get("result") != 0:
        raise Exception(f"pCloud upload failed: {data}")

    metadata = data.get("metadata")
    if isinstance(metadata, list):
        metadata = metadata[0]

    return metadata["fileid"]
