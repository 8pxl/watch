from cache import Cache
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import requests

def getWebsites():
    return [line.rstrip() for line in open("sites.txt", 'r').readlines()]

def readWebsite(url, driver):
    driver.get(url)
    text = driver.find_element(By.TAG_NAME, "body").text
    # pageSource = driver.page_source
    # print(pageSource)
    # print(text)
    return(text)
    # return(requests.get(url, timeout=10).text)

def notify(title, content):
    notif = f'display notification "{content}" with title "{title}"'
    subprocess.run([
        "osascript",
        "-e",
        notif
    ])
#init
notify("watch", "process started!")
if __name__ == "__main__":
    notify("watch", "process started!")
    websites = getWebsites()

    cache = Cache(websites)
    contents = cache.readCache()

    # web stuff
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)
    #event loop
    while True:
        for website, content in contents.items():
            url = website
            hashedContent = cache.createHash(readWebsite(website, driver))
            if (hashedContent != content):
                cache.updateCache(url, hashedContent)
                contents[website] = hashedContent
                print(f"update has occured! in {website}")
                notify("watch", f"update has occured! in {website}")
        time.sleep(4)
    driver.quit()
