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
import setuptools.dist
import undetected_chromedriver as uc

class WebScrapeInfo:
    def __init__(self, url, checkForTextInRomName, fileName):
        self.url = url
        self.checkForTextInRomName = checkForTextInRomName
        self.fileName = fileName


baseUrl = "https://www.romhacking.net"
itemsToScrape = [WebScrapeInfo(baseUrl + "/?page=translations&languageid=12&perpage=200", "english", "ROMHacking_TranslationUrls.txt"),
                 WebScrapeInfo(baseUrl + "/?page=hacks&languageid=12&perpage=200", "", "ROMHacking_RomHackUrls.txt"),
                 WebScrapeInfo(baseUrl + "/?page=homebrew&languageid=12&perpage=200", "", "ROMHacking_HomeBrewUrls.txt")]

webdriverOptions = webdriver.ChromeOptions()
#webdriverOptions.add_argument("user-data-dir=C:/Temp/User Data")
#webdriverOptions.add_argument("profile-directory=Default")
#webdriverOptions.add_argument("start-maximized")
#webdriverOptions.add_argument("disable-infobars")
#webdriverOptions.add_argument("--disable-extensions")
#webdriverOptions.add_argument("--disable-gpu")
#webdriverOptions.add_argument("--disable-dev-shm-usage")
#webdriverOptions.add_argument("--no-sandbox")
#webdriverOptions.add_argument("start-maximized")
#webdriverOptions.add_experimental_option("excludeSwitches", ["enable-automation"])
#webdriverOptions.add_experimental_option('useAutomationExtension', False)
webDriverInfo = uc.Chrome(options=webdriverOptions)

def GetBeautifulSoupInfo(isPageSource, url):
    htmlData = ''
    if isPageSource:
        htmlData = url
    else:
        response = requests.get(url)
        htmlData = response.text
    soup = BeautifulSoup(htmlData, "html.parser")
    return soup

def GetNextButton(soup: BeautifulSoup):
    pages = soup.find(class_="pages")
    return pages.find("a", string="Next")

def GetNextButtonUrl(buttonItem: BeautifulSoup):
    return baseUrl + buttonItem['href']

def GetGameItems(soup: BeautifulSoup):
    tableItem = soup.find(name="tbody")
    return tableItem.findAll(name="tr")

def GetGameUrlFromGameItem(gameItem: BeautifulSoup):
    return baseUrl + gameItem.find(name="a")['href']

def GetGamePlatformFromGameItem(gameItem: BeautifulSoup):
    return gameItem.find(class_="Platform").text

def GetGameNameFromGameItem(gameItem: BeautifulSoup):
    return gameItem.find(name="a").text

for itemToScrape in itemsToScrape:
    nextButtonExists = True
    if os.path.exists(itemToScrape.fileName):
        os.remove(itemToScrape.fileName)
    webDriverInfo.get(itemToScrape.url)
    while nextButtonExists:
        time.sleep(7) # cloudflare giving some push back, gotta go slow
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