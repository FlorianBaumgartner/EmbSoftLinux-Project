import os
import json
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

class ChatGptX:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.headless = True          # run browser in headless mode
        self.driver = webdriver.Chrome(options=chrome_options)

    def __del__(self):
        self.driver.quit()
    
    def generate(self, prompt):
        regenerating = 5
        for i in range(regenerating):
            self.driver.get("https://chatgptx.de/")
            self.driver.set_window_size(1200, 1072)
            self.driver.find_element(By.ID, "prompt").click()
            self.driver.find_element(By.ID, "prompt").send_keys("Der user will ein lied hören. Konvertiere mir seine Kernaussage als JSON ausdruck im stil von \"Artist\" und \"Title\". Falls nur eines der beiden genannt wird, soll das andere feld jeweils leer sein. Folgendes ist seine formulierung: Hallo ich würde gerne ein Lied von Coldplay hören, am meisten gefällt mir Yellow.")
            self.driver.find_element(By.ID, "sendchat_btn").click()

            timeout = 100
            while True:
                try:
                    state = self.driver.find_element(By.ID, "regenerate")       # Return at start "NEW" and then "Stop generating"
                    if state.is_displayed():
                        break
                except Exception as e:
                    pass
                time.sleep(0.1)
                timeout -= 1
                if timeout == 0:
                    raise Exception("Timeout")
            
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            target_div = soup.find('div', class_='markdown prose w-full break-words dark:prose-invert dark system_write')
            if target_div:
                answer = target_div.get_text(strip=True)
            
            if answer.startswith("Bitte versuchen Sie es"):
                print("ChatGptX is currently not available. Try again in 1 second.")
                time.sleep(1.0)
                continue
            else:
                return answer
        raise Exception("ChatGptX not available")


if __name__ == "__main__":
    prompt = """Der user will ein lied hören. Konvertiere mir seine Kernaussage als JSON ausdruck im stil von "Artist" und "Title". Falls nur eines der beiden genannt wird, soll das andere feld jeweils leer sein. Folgendes ist seine formulierung: Hallo ich würde gerne ein Lied von Coldplay hören, am meisten gefällt mir Yellow."""
    # prompt = "Ist Linux besser als Windows?"

    gpt = ChatGptX()
    answer = gpt.generate(prompt)
    print(answer)

