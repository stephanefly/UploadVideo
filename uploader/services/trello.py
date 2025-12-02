import requests
from django.conf import settings

def create_trello_card(title: str, description: str, uploader: str) -> str:
    """
    Crée une carte Trello avec un label issu de l'uploader (minuscule).
    """
    # Convertir uploader → label Trello
    label_name = uploader.lower()

    # 1. Vérifier si le label existe déjà sur le board
    url_labels = f"https://api.trello.com/1/boards/yhA3ZL3R/labels"
    params_auth = {
        "key": settings.TRELLO_KEY,
        "token": settings.TRELLO_TOKEN,
    }
    r = requests.get(url_labels, params=params_auth)
    labels = r.json()

    # 2. Chercher un label portant le même nom
    label_id = None
    for lbl in labels:
        if lbl.get("name", "").lower() == label_name:
            label_id = lbl["id"]
            break

    # 3. S’il n'existe pas → on le crée
    if label_id is None:
        url_create_label = "https://api.trello.com/1/labels"
        params_label = {
            "key": settings.TRELLO_KEY,
            "token": settings.TRELLO_TOKEN,
            "idBoard": settings.TRELLO_BOARD_ID,
            "name": label_name,
            "color": "grey",
        }
        r = requests.post(url_create_label, params=params_label)
        label_id = r.json()["id"]

    # 4. Création carte + label auto
    url_card = "https://api.trello.com/1/cards"
    params_card = {
        "idList": settings.TRELLO_LIST_ID,
        "name": title,
        "desc": description,
        "idLabels": label_id,
        "key": settings.TRELLO_KEY,
        "token": settings.TRELLO_TOKEN,
    }

    r = requests.post(url_card, params=params_card)
    data = r.json()

    if "url" not in data:
        raise Exception(f"Trello error: {data}")
    return data["url"]
