import os.path
import sys
import requests
import zipfile
from bs4 import BeautifulSoup
from datetime import datetime
from tqdm import tqdm
import pygetwindow as gw
import os
import time
import math
from selenium import webdriver
from selenium.webdriver import chrome
from selenium.webdriver.common.by import By

os.system('title "ESDEGameRomDownload"')

romPath = sys.argv[1]
gameName = sys.argv[2]
systemName = sys.argv[3]
systemFullName = sys.argv[4]

def GetBeautifulSoupInfo(isPageSource, url):
    htmlData = ''
    if isPageSource:
        htmlData = url
    else:
        response = requests.get(url)
        htmlData = response.text
    soup = BeautifulSoup(htmlData, "html.parser")
    time.sleep(0.5) # don't flood the scraper
    return soup

f = open('c:\\temp\\logging.txt', 'a')
f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
f.write('\n')
f.write(romPath)
f.write('\n')
f.write(gameName)
f.write('\n')
f.write(systemName)
f.write('\n')
f.write(systemFullName)
f.write('\n')
f.write('\n')
f.close()

try:
    gw.getWindowsWithTitle('ESDEGameRomDownload')[0].activate()
    host = ""
    url = ""
    with open(romPath, 'r') as file:
        firstLine = file.readline()
        if firstLine != "ESDE Placeholder\n":
            sys.exit(0)
        allLines = file.read().splitlines()
        if len(allLines) < 2:
            sys.exit(0)
        host = allLines[0]
        url = allLines[1]
    os.remove(romPath)
    downloadPath = ""
    if host == "myrient":
        downloadPath = url
    if host == "ROMHacking":
        splitPath = url.split("/")
        downloadPath = "https://www.romhacking.net/download/" + splitPath[-2] +  "/" + splitPath[-1]
    if host == "RetroGameTalk":
        webdriverOptions = webdriver.ChromeOptions()
        webdriverOptions.add_argument("user-data-dir=C:/Temp/User Data")
        webdriverOptions.add_argument("profile-directory=Default")
        webdriverOptions.add_argument("start-maximized")
        webdriverOptions.add_argument("disable-infobars")
        webdriverOptions.add_argument("--disable-extensions")
        webdriverOptions.add_argument("--disable-gpu")
        webdriverOptions.add_argument("--disable-dev-shm-usage")
        webdriverOptions.add_argument("--no-sandbox")
        webDriverInfo = webdriver.Chrome(options=webdriverOptions)
        webDriverInfo.get(url)
        showLinksButton = webDriverInfo.find_element(by=By.CLASS_NAME, value="acf-get-content-button")
        showLinksButton.click()
        time.sleep(0.5) # give the page time to load
        childSoup = GetBeautifulSoupInfo(True, webDriverInfo.page_source)
        platformInfo = childSoup.find(itemprop="gamePlatform operatingSystem").text
        infoTableItems = childSoup.find(class_="rom-info").find(name="tbody").findAll(name="tr")
        downloadLinksTable = childSoup.find(class_="download-links table")
        downloadLinks = downloadLinksTable.find_all(name="a")
        for downloadLink in downloadLinks:
            fileNameWithExtension = downloadLink.text
            if fileNameWithExtension is None:
                continue
            downloadUrl = downloadLink['href']
            if 'english' in fileNameWithExtension.lower():
                break
    with requests.get(url, stream=True) as requestInfo:
        zipName = romPath
        if not zipName.endswith(".zip"):
            zipName += ".zip"
        with open(zipName, "wb") as file:
            pbar = tqdm(unit="B", unit_scale=True, unit_divisor=1024, total=int(requestInfo.headers['Content-Length']))
            pbar.clear()
            for chunk in requestInfo.iter_content(chunk_size=1024):
                if chunk:
                    pbar.update(len(chunk))
                    file.write(chunk)
            pbar.close()
    if not romPath.endswith(".zip"):
        with zipfile.ZipFile(zipName, 'r') as zipRef:
            zipOutputDirectory = os.path.dirname(romPath)
            zipRef.extractall(zipOutputDirectory)
        os.remove(zipName)
    #os.rename(romPath, zipName)
    if requestInfo.status_code == 200:
        
        #list_of_files = glob.glob('/path/to/folder/*') # * means all if need specific format then *.csv
        #latest_file = max(list_of_files, key=os.path.getctime)
        #os.rename(latest_file, romPath)
        print(f"File '{romPath}' downloaded successfully.")

    else:
        print(f"Failed to download file. Status code: {requestInfo.status_code}")
except FileNotFoundError:
    print("Error: The file 'your_file.txt' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")
    time.sleep(5)

gw.getWindowsWithTitle('ES-DE')[0].activate()