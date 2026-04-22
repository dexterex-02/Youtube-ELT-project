import requests
import json
import os
from dotenv import load_dotenv
from datetime import date

load_dotenv(dotenv_path="./.env")

API = os.getenv("API")
YOUTUBE_HANDLE = os.getenv("YOUTUBE_HANDLE")
maxResults = 50

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
    
def get_videoId(playlistid):
    video_ids = []
    base_API = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlistid}&key={API}"
    pageToken = None

    try:
        while True:
            url = base_API
            if pageToken:
                url+=f"&pageToken={pageToken}"

            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            for item in data.get("items",[]):
                video_id = item["contentDetails"]["videoId"]
                video_ids.append(video_id)

            pageToken = data.get("nextPageToken")

            if not pageToken:
                break
            
        return video_ids
    
    except requests.exceptions.RequestException as e:
        raise e




def extract_video_data(videoIDs):
    extracted_data =[]
    def batch_list(videoIDsList, batch_size):
        for videoid in range(0, len(videoIDsList), batch_size):
            yield videoIDsList[videoid : videoid + batch_size]

    try:
        for batch in batch_list(videoIDs, maxResults):
            video_ids_str = ",".join(batch)
            
            url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=statistics&part=snippet&id={video_ids_str}&key={API}"

            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            for item in data.get("items", []):
                video_id = item["id"]
                snippet = item["snippet"]
                contentDetails = item["contentDetails"]
                statistics = item["statistics"]

                video_data = {
                    "video_id" : video_id,
                    "title" : snippet["title"],
                    "publishedAt" : snippet["publishedAt"],
                    "duration" : contentDetails["duration"],
                    "viewCount" : statistics.get("viewCount", None),
                    "likeCount" : statistics.get("likeCount", None),
                    "commentCount" : statistics.get("commentCount", None)
                }

                extracted_data.append(video_data)

        return extracted_data
    
    except requests.exceptions.RequestException as e:
        raise e

def save_toJson(extracted_data):
    filepath = f"./data/YT_Data_{date.today()}.json"

    with open(filepath, "w", encoding= "utf-8") as jsonOutput:
        json.dump(extracted_data, jsonOutput, indent= 4, ensure_ascii= False)



if __name__ == "__main__":
    playlistid = get_Playlistid()
    videoIDs = get_videoId(playlistid)
    video_data = extract_video_data(videoIDs)
    save_toJson(video_data)

