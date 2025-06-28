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

itemsToScrape = [WebScrapeInfo("https://retrogametalk.com/repository/translations/", "english", "TranslationUrls.txt"),
                 WebScrapeInfo("https://retrogametalk.com/repository/romhacks/", "", "RomHackUrls.txt")]

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

for itemToScrape in itemsToScrape:
    nextButtonExists = True
    webDriverInfo.get(itemToScrape.url)
    while nextButtonExists:
        soup = GetBeautifulSoupInfo(True, webDriverInfo.page_source)
        gamesOnPage = soup.find_all(class_="game-container")
        nextButton = soup.find(class_="next page-numbers")
        for gameOnPage in gamesOnPage:
            linkItem = gameOnPage.find(name="a")
            webDriverInfo.get(linkItem['href'])
            showLinksButton = webDriverInfo.find_element(by=By.CLASS_NAME, value="acf-get-content-button")
            showLinksButton.click()
            time.sleep(0.5) # give the page time to load
            childSoup = GetBeautifulSoupInfo(True, webDriverInfo.page_source)
            platformInfo = childSoup.find(itemprop="gamePlatform operatingSystem").text
            infoTableItems = childSoup.find(class_="rom-info").find(name="tbody").findAll(name="tr")
            downloadLinksTable = childSoup.find(class_="download-links table")
            if downloadLinksTable is None:
                continue
            downloadLinks = downloadLinksTable.find_all(name="a")
            for downloadLink in downloadLinks:
                fileNameWithExtension = downloadLink.text
                if fileNameWithExtension is None or not itemToScrape.checkForTextInRomName.lower() in fileNameWithExtension.lower():
                    continue
                downloadUrl = downloadLink['href']
                with open(itemToScrape.fileName, "a+") as romFile:
                    fileNameWithoutExtension, fileExtension = os.path.splitext(fileNameWithExtension)
                    romFile.write(downloadUrl + "\t" + fileNameWithoutExtension + "\t" + platformInfo + "\n")
        if nextButton is None:
            nextButtonExists = False
        else:
            webDriverInfo.get(nextButton['href'])
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    