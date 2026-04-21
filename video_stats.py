import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

API = os.getenv("API")
YOUTUBE_HANDLE = os.getenv("YOUTUBE_HANDLE")


def get_Playlistid():

    try:
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={YOUTUBE_HANDLE}&key={API}"
        response = requests.get(url)
        # print(response)
        response.raise_for_status()
        data = response.json()
        # print(json.dumps(data, indent= 4))
        channel_playlist = data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        print(channel_playlist)

        return channel_playlist
    
    except requests.exceptions.RequestException as e:
        raise e

if __name__ == "__main__":
    get_Playlistid()
