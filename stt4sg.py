import os
import json
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Stt4Sg:
    def __init__(self, downloadDir = Path(__file__).parent / "download"):
        self.downloadDir = downloadDir
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('prefs', {
            "download.default_directory": str(downloadDir),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True
        })

        chrome_options.headless = True          # run browser in headless mode
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 60)

    def __del__(self):
        self.driver.quit()

    def getTranscript(self, file):
        self.driver.get("https://stt4sg.fhnw.ch/long")
        self.driver.set_window_size(987, 1068)

        # Waiting for the file input to be present and sending the file path
        file_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".file-input")))
        file_input.send_keys(str(file))

        # Assuming you want to click a link with text ".JSON", wait for it to be clickable then click
        json_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, ".JSON")))
        json_link.click()

        # Wait for the file to be downloaded
        while True:
            files = os.listdir(self.downloadDir)
            if len(files) > 0 and files[0].endswith(".json"):
                with open(self.downloadDir / files[0], encoding="utf-8") as json_file:
                    data = json.load(json_file)
                for f in files:
                    os.remove(self.downloadDir / f)
                break

        transcript = data[0]["transcript"]
        return transcript


if __name__ == "__main__":
    stt4sg = Stt4Sg()
    transcript = stt4sg.getTranscript(Path(__file__).parent / "test.mp3")
    print(transcript)
