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

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Youtube:
    def __init__(self):
        self.processHandle = None
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.headless = True          # run browser in headless mode
        self.driver = webdriver.Chrome(options=chrome_options)

    def __del__(self):
        self.driver.quit()
        
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
        base_url = "https://music.youtube.com/search"
        query_param = urllib.parse.quote_plus(query)
        url = f"{base_url}?q={query_param}"

        self.driver.get(url)
        self.driver.find_element(By.CSS_SELECTOR, "#yDmH0d > c-wiz > div > div > div > div.NIoIEf > div.G4njw > div.qqtRac > div.VtwTSb > form:nth-child(3) > div > div > button").click()
        time.sleep(2.5)     # TODO: Make better; wait untl the page is loaded
        page = self.driver.page_source
        return "https://www.youtube.com/" + page[page.find("watch?"):].split('"')[0]


    def play_audio(self, video_url):
        # Use youtube-dl to get the audio stream URL and play it with mpv
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
