import os
import json
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

class PseudoGpt:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.headless = True          # run browser in headless mode
        self.driver = webdriver.Chrome(options=chrome_options)

    def __del__(self):
        self.driver.quit()
    
    def generate(self, prompt):
        self.driver.get("https://huggingface.co/chat/")
        self.driver.set_window_size(988, 1070)
        self.driver.find_element(By.CSS_SELECTOR, ".m-0").click()
        self.driver.find_element(By.CSS_SELECTOR, ".m-0").send_keys(prompt)
        self.driver.find_element(By.CSS_SELECTOR, ".mx-1 path").click()
        time.sleep(1.0)

        timeout = 100
        while True:
            try:
                state = self.driver.find_element(By.CSS_SELECTOR, ".py-1").text       # Return at start "NEW" and then "Stop generating"
            except Exception as e:
                break
            time.sleep(0.1)
            timeout -= 1
            if timeout == 0:
                raise Exception("Timeout")

        answer = ""
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        target_div = soup.find('div', class_='prose max-w-none dark:prose-invert max-sm:prose-sm prose-headings:font-semibold prose-h1:text-lg prose-h2:text-base prose-h3:text-base prose-pre:bg-gray-800 dark:prose-pre:bg-gray-900')
        if target_div:
            answer = target_div.get_text(strip=True)
        return answer


if __name__ == "__main__":
    prompt = """Der user will ein lied hören. Konvertiere mir seine Kernaussage als JSON ausdruck im stil von "Artist" und "Title". Falls nur eines der beiden genannt wird, soll das andere feld jeweils leer sein. Folgendes ist seine formulierung: Hallo ich würde gerne ein Lied von Coldplay hören, am meisten gefällt mir Yellow."""
    # prompt = "Ist Linux besser als Windows?"

    gpt = PseudoGpt()
    answer = gpt.generate(prompt)
    print(answer)

