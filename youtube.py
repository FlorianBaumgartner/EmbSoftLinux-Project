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
import html


class Youtube:
    def _init_(self):
        self.processHandle = None
        
    def playMusic(self, search_query, url_type_music=True): 
        #Youtube Music
        if(url_type_music == True):
            video_url = self.get_video_url_music(search_query)
            if(video_url == ""):
                return ""
            else:
                print(f"Playing {video_url}")
                self.play_audio(video_url)
                title = self.getTitle(video_url)
                return title
        #Youtube Video
        else:
            video_url=self.get_video_url(search_query)
            print(f"Playing {video_url}")
            self.play_audio(video_url)
            title = self.getTitle(video_url)
            return title
        
    def getTitle(self, url):
        page_bytes = requests.get(url).content

        page = page_bytes.decode("utf-8")
        # Find the start and end indexes of the title tag
        title_start = page.find("<title>") + len("<title>")
        title_end = page.find("</title>", title_start)

        if title_start != -1 and title_end != -1:
            # Extract the text between the title tags
            video_title = page[title_start:title_end]
            # print("Title = " + html.unescape(video_title))

            title = html.unescape(video_title)
            if(title.strip().endswith("- YouTube")):
                title = title.strip()[:-10]
            return title
        else:
            print("Video title not found.")
            return ""

    def stopMusic(self):
        if self.processHandle:
            self.processHandle.terminate()
            self.processHandle = None

    def getPlayStatus(self):
        if self.processHandle:
            ret = self.processHandle.poll()
            return ret is None
        else:
            return False

    def get_video_url(self, query):
        base_url = "https://www.youtube.com/results"
        query_param = urllib.parse.quote_plus(query)
        url = f"{base_url}?search_query={query_param}&sp=EgIQAQ%253D%253D"
        page = str(requests.get(url).content)
        return "https://www.youtube.com/" + page[page.find("/watch?"):].split('\\')[0]
    
    def get_video_url_music(self, query):
        retryCount = 50
        base_url = "https://search.yahoo.com/search"
        query = f"{query} site:music.youtube.com"
        query_param = urllib.parse.quote_plus(query)
        url = f"{base_url}?q={query_param}"
        print(f"Query URL: {url}")
        while True:
            page = str(requests.get(url).content)
            if(page.find("/watch?")) != -1: 
                return "https://www.youtube.com" + page[page.find("/watch?"):].split('"')[0]
            else:
                print(f"Could not find video URL. Retrying {retryCount} times")
                retryCount -= 1
                time.sleep(0.1)
            if retryCount == 0:
                return ""

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
    # title = youtube.playMusic("Funniest 5 Second Video Ever!", False)
    title = youtube.playMusic("Meduza Lose Control", True)
    print(f"Title: {title}")
    # while True:
    #     playState = youtube.getPlayStatus()
    #     print(f"Play State: {playState}")
    #     if playState == 0:
    #         break
    #     time.sleep(0.1)

    input("\n\nPress enter to stop playing")
    youtube.stopMusic()