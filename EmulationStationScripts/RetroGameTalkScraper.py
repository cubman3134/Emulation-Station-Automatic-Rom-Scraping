import os.path
import requests
from bs4 import BeautifulSoup
import os.path
import os
import glob
import sys
from pathlib import Path
from datetime import datetime, timedelta
import time
from selenium import webdriver
from selenium.webdriver import chrome
from selenium.webdriver.common.by import By

class WebScrapeInfo:
    def __init__(self, url, checkForTextInRomName, fileName):
        self.url = url
        self.checkForTextInRomName = checkForTextInRomName
        self.fileName = fileName


baseUrl = "https://retrogametalk.com"
itemsToScrape = [WebScrapeInfo(baseUrl + "/repository/translations/", "english", "RetroGameTalk_TranslationUrls.txt"),
                 WebScrapeInfo(baseUrl + "/repository/romhacks/", "", "RetroGameTalk_RomHackUrls.txt")]

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

def GetNextButton(soup: BeautifulSoup):
    return soup.find(class_="next page-numbers")

def GetNextButtonUrl(buttonItem: BeautifulSoup):
    return buttonItem['href']

def GetGameItems(soup: BeautifulSoup):
    return soup.find_all(class_="game-container")

def GetGameUrlFromGameItem(gameItem: BeautifulSoup):
    return gameItem.find(name="a")['href']

def GetGamePlatformFromGameItem(gameItem: BeautifulSoup):
    return gameItem.find(class_="console").text

def GetGameNameFromGameItem(gameItem: BeautifulSoup):
    return gameItem.find(class_="game-title").text

for itemToScrape in itemsToScrape:
    nextButtonExists = True
    if os.path.exists(itemToScrape.fileName):
        os.remove(itemToScrape.fileName)
    webDriverInfo.get(itemToScrape.url)
    while nextButtonExists:
        time.sleep(1)
        soup = GetBeautifulSoupInfo(True, webDriverInfo.page_source)
        gamesOnPage = GetGameItems(soup)
        nextButton = GetNextButton(soup)
        for gameOnPage in gamesOnPage:
            downloadUrl = GetGameUrlFromGameItem(gameOnPage)
            platformInfo = GetGamePlatformFromGameItem(gameOnPage)
            gameName = GetGameNameFromGameItem(gameOnPage)
            with open(itemToScrape.fileName, "a+", encoding="utf-8") as romFile:
                romFile.write(downloadUrl + "\t" + gameName + "\t" + platformInfo + "\n")
        if nextButton is None:
            nextButtonExists = False
        else:
            webDriverInfo.get(GetNextButtonUrl(nextButton))
    
sys.exit(0)