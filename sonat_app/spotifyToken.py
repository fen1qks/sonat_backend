import time
import base64
import requests

CLIENT_ID = "3d1255be2a594a59b27e283c2bc13481"
CLIENT_SECRET = "ee31b7b58f834ba586e104c6cd45fe0c"

spotify_token = None
spotify_token_expires_at = 0


def get_spotify_token():
    global spotify_token, spotify_token_expires_at

    now = time.time()

    if spotify_token and now < spotify_token_expires_at:
        return spotify_token

    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_base64 = base64.b64encode(auth_string.encode()).decode()

    response = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={
            "Authorization": f"Basic {auth_base64}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={"grant_type": "client_credentials"},
        timeout=10,
    )

    response.raise_for_status()
    data = response.json()

    spotify_token = data["access_token"]
    spotify_token_expires_at = now + data["expires_in"] - 30

    return spotify_token