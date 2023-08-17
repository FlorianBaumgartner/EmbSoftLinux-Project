# Remove youtube-dl as yt-dlp is newer and works better
#
# sudo apt remove youtube-dl
# pip uninstall youtube-dl
# python3 -m pip install -U yt-dlp
# 
# Create symbolic link: sudo ln -s $(which yt-dlp) /usr/local/bin/youtube-dl
# Test with: mpv --no-video --ytdl-format=bestaudio https://www.youtube.com/watch?v=z1fadkdxAX0


import time
import subprocess
from pathlib import Path
import requests
import urllib.parse


class Youtube:
    def __init__(self):
        self.processHandle = None
        
    def playMusic(self, search_query):
        video_url = self.get_video_url_music(search_query)
        print(f"Playing {video_url}")
        self.play_audio(video_url)

    def stopMusic(self):
        if self.processHandle:
            self.processHandle.terminate()
            self.processHandle = None

    def get_video_url(self, query):
        base_url = "https://www.youtube.com/results"
        query_param = urllib.parse.quote_plus(query)
        url = f"{base_url}?search_query={query_param}&sp=EgIQAQ%253D%253D"
        page = str(requests.get(url).content)
        return "https://www.youtube.com/" + page[page.find("/watch?"):].split('\\')[0]
    
    def get_video_url_music(self, query):
        base_url = "https://www.bing.com/search"
        query = f"{query} site:music.youtube.com"
        query_param = urllib.parse.quote_plus(query)
        url = f"{base_url}?q={query_param}"
        page = str(requests.get(url).content)
        return "https://www.youtube.com" + page[page.find("/watch?"):].split('"')[0]

    def play_audio(self, video_url):
        command = [
            'mpv',
            '--no-video',
            '--ytdl-format=bestaudio',
            video_url
        ]
        self.processHandle = subprocess.Popen(command)


if __name__ == "__main__":
    youtube = Youtube()
    youtube.playMusic("David Guetta Blue")
    time.sleep(20)
    youtube.stopMusic()
