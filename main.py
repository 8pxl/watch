from cache import Cache
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re

debugCount = 0

def getWebsites():
    return [line.rstrip() for line in open("sites.txt", 'r').readlines()]

def readWebsite(url, driver):
    global debugCount
    ignoreNumbers = True
    driver.get(url)
    text = driver.find_element(By.TAG_NAME, "body").text
    if ignoreNumbers:
        text = re.sub(r'\d+', '', text)

    # f = open(f"data/{len(url)} {debugCount}", 'x')
    # f.write(text)

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

def printInfo(websites):
    print("watching the following:")
    for website in websites:
        print(website)
    print("")

#init
if __name__ == "__main__":
    notify("watch", "process started!")

    websites = getWebsites()
    cache = Cache(websites)
    contents = cache.readCache()

    printInfo(websites)


    # web stuff
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)

    #event loop
    while True:
        debugCount +=1
        for website, content in contents.items():
            hashedContent = cache.createHash(readWebsite(website, driver))
            if (hashedContent != content):
                cache.updateCache(website, hashedContent)
                contents[website] = hashedContent
                # print(hashedContent)
                # print(f"count: {debugCount}")
                print(f"update has occured! in {website}")
                notify("watch", f"update has occured! in {website}")
        time.sleep(4)
