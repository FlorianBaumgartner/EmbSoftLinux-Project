import time
from googleapiclient.discovery import build
import subprocess
from pathlib import Path

class Youtube:
    def __init__(self, apiKeyPath = Path(__file__).parent / "api_key.secret"):
        self.retryCount = 20
        with open(apiKeyPath, 'r') as f:
            self.API_KEY = f.read()
        
    def playMusic(self, search_query):
        video_url = self.get_video_url(self.API_KEY, search_query)
        print(f"Playing {video_url}")
        for i in range(self.retryCount):
            try:
                ret = self.play_audio(video_url)
                if(ret.returncode != 0):
                    print("Could not start playing audio -> retrying")
                    raise Exception("mpv returned non-zero exit code")
                break
            except:
                time.sleep(0.5)

    def get_video_url(self, api_key, search_query):
        # Build the YouTube API client
        youtube = build('youtube', 'v3', developerKey=api_key)

        # Search for videos matching the query
        search_response = youtube.search().list(
            q=search_query,
            part='id,snippet',
            maxResults=3
        ).execute()

        # Extract video ID from the first result
        for i in range(len(search_response['items'])):
            try:
                video_id = search_response['items'][i]['id']['videoId']
                break
            except:
                pass

        video_url = f"https://www.youtube.com/watch?v={video_id}"
        return video_url

    def play_audio(self, video_url):
        # Use youtube-dl to get the audio stream URL and play it with mpv
        command = [
            'mpv',
            '--no-video',
            '--ytdl-format=bestaudio',
            video_url
        ]
        ret = subprocess.run(command)
        return ret


if __name__ == "__main__":
    youtube = Youtube()
    youtube.playMusic("Michael Jackson (Audio)")
