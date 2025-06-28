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

dateFormatString = "%Y-%m-%d %H:%M:%S"
#begin debug lines, delete
f = open('c:\\temp\\logging.txt', 'a')
f.write(datetime.now().strftime(dateFormatString))
f.write('\n')
f.write('\n')
f.close()
#end debug lines, delete

def GetBeautifulSoupInfo(isPageSource, url):
    time.sleep(0.5)
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
    webDriverInfo.get(itemToScrape.url)
    soup = GetBeautifulSoupInfo(True, webDriverInfo.page_source)
    #allLinks = soup.find_all(name="td", class_="link")
    gamesOnPage = soup.find_all(class_="game-container")
    nextButton = soup.find(class_="next page-numbers")
    for gameOnPage in gamesOnPage:
        linkItem = gameOnPage.find(name="a")
        webDriverInfo.get(linkItem['href'])
        showLinksButton = webDriverInfo.find_element(by=By.CLASS_NAME, value="acf-get-content-button")
        showLinksButton.click()
        time.sleep(1)
        childSoup = GetBeautifulSoupInfo(True, webDriverInfo.page_source)
        platformInfo = childSoup.find(itemprop="gamePlatform operatingSystem").text
        infoTableItems = childSoup.find(class_="rom-info").find(name="tbody").findAll(name="tr")
        #imageFormat = ''
        #for infoTableItem in infoTableItems:
        #    headerItem = infoTableItem.find(name="th")
        #    valueItem = infoTableItem.find(name="td")
        #    if (headerItem.text == "Image Format"):
        #        imageFormat = valueItem.Text

        downloadLinksTable = childSoup.find(class_="download-links table")
        if downloadLinksTable is None:
            continue
        downloadLinks = downloadLinksTable.find_all(name="a")
        for downloadLink in downloadLinks:
            fileNameWithExtension = downloadLink.text
            if fileNameWithExtension is None or not itemToScrape.checkForTextInRomName.lower() in fileNameWithExtension.lower():
                continue
            downloadUrl = downloadLink['href']

        size = sizeItem.getText()
        if size is None or size == "-":
            continue
        filePath = os.path.join(systemRomPath, title + systemLink.fileType)
        if os.path.isfile(filePath):
            continue
        with open(filePath, "w") as romFile:
            romFile.write("ESDE Placeholder\n")
            romFile.write("myrient\n") # in case I add others in the future, we know how to take each apart
            romFile.write(systemLink.url + hrefValue + "\n")
            romFile.write(size) # not sure if this is important but too much info isn't an issue
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    