import requests
from bs4 import BeautifulSoup
import os.path
import os
import glob
import sys
from pathlib import Path
from datetime import datetime, timedelta
import time

class LocalFileScrapingInfo:
    def __init__(self, fileType, directoryPath):
        self.fileType = fileType
        self.directoryPath = directoryPath

class SystemInfo:
    def __init__(self, url, fileType, emulatorAliases, zipAllowed):
        self.url = url
        self.fileType = fileType
        self.emulatorAliases = emulatorAliases
        self.zipAllowed = zipAllowed

#systemName = sys.argv[1]
#systemFullName = sys.argv[2]
#systemRomPath = sys.argv[3]


def TryWriteRomFile(filePath, siteName, url):
    if os.path.isfile(filePath):
        return
    with open(filePath, "w") as romFile:
        romFile.write("ESDE Placeholder\n")
        romFile.write(siteName + "\n")
        romFile.write(url + "\n")

itemsToScrape = [LocalFileScrapingInfo("RomHacks", "../../settings/RomHackFiles"),
                 LocalFileScrapingInfo("Translations", "../../settings/TranslationFiles")]

#all files at https://myrient.erista.me/files/No-Intro/
systemLinks = {
        "3do": SystemInfo("https://myrient.erista.me/files/TOSEC-ISO/3DO/3DO%20Interactive%20Multiplayer/Games/", ".bin", ['3DO'], False),
        #"atari2600": SystemInfo("https://myrient.erista.me/files/No-Intro/Atari%20-%202600/", ".zip", ['2600'], True),
        #"atari5200": SystemInfo("https://myrient.erista.me/files/No-Intro/Atari%20-%205200/", ""),
        #"atari7800": SystemInfo("https://myrient.erista.me/files/No-Intro/Atari%20-%207800/", "", ['7800']),
        #"atarijaguar": SystemInfo("https://myrient.erista.me/files/No-Intro/Atari%20-%20Jaguar%20%28ROM%29/", "", ['JAG']),
        #"atarijaguarcd": SystemInfo("https://myrient.erista.me/files/TOSEC-ISO/Atari/Jaguar%20CD/Games/", ""),
        #"atarilynx": SystemInfo("https://myrient.erista.me/files/No-Intro/Atari%20-%20Lynx%20%28LYX%29/", "", ['LYNX']),
        #"c64": SystemInfo("https://myrient.erista.me/files/No-Intro/Commodore%20-%20Commodore%2064/", ""),
        #"dreamcast": SystemInfo("https://myrient.erista.me/files/Redump/Sega%20-%20Dreamcast/", "", ['EGA Dreamcast', 'DC']),
        #"famicom": SystemInfo("https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Family%20Computer%20Disk%20System%20(FDS)/", "", ['FDS']),
        #"gameandwatch": SystemInfo("https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Game%20%26%20Watch/", ""),
        #"gamegear": SystemInfo("https://myrient.erista.me/files/No-Intro/Sega%20-%20Game%20Gear/", "", ['Game Gear', 'GG']),
        #"gb": SystemInfo("https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Game%20Boy/", "", ['GameBoy', 'GB']),
        #"gba": SystemInfo("https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Game%20Boy%20Advance/", ".zip", ['GBA']),
        #"gbc": SystemInfo("https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Game%20Boy%20Color/", "", ['GB Color', 'GBC']),
        #"gc": SystemInfo("https://myrient.erista.me/files/Redump/Nintendo%20-%20GameCube%20-%20NKit%20RVZ%20[zstd-19-128k]/", "", ['Gamecube', 'GCN', 'GC']),
        #"genesis": SystemInfo("https://myrient.erista.me/files/No-Intro/Sega%20-%20Mega%20Drive%20-%20Genesis/", "", ['SEGA Genesis', 'Genesis', 'GEN']),
        #"intellivision": SystemInfo("https://myrient.erista.me/files/No-Intro/Mattel%20-%20Intellivision/", ""),
        #"mame": SystemInfo("https://myrient.erista.me/files/Internet%20Archive/chadmaster/mame-merged/mame-merged/", "", ['ARC']),
        #"mastersystem": SystemInfo("https://myrient.erista.me/files/No-Intro/Sega%20-%20Master%20System%20-%20Mark%20III/", "", ['Master System', 'SMS']),
        #"msx": SystemInfo("https://myrient.erista.me/files/No-Intro/Microsoft%20-%20MSX/", "", ['MSX']),
        "n3ds": SystemInfo("https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Nintendo%203DS%20(Decrypted)/", ".3ds", ['3DS'], True),
        "n64": SystemInfo("https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Nintendo%2064%20(ByteSwapped)/", ".n64", ['N64'], True),
        "nds": SystemInfo("https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Nintendo%20DS%20(Decrypted)/", ".nds", ['DS', 'NDS'], True),
        "neogeo": SystemInfo("https://myrient.erista.me/files/TOSEC/SNK/Neo-Geo/Games/", ".neo", ['NG'], True),
        "neogeocd": SystemInfo("https://myrient.erista.me/files/Redump/SNK%20-%20Neo%20Geo%20CD/", ".cue", ['NEO-GEO CD', 'NGCD'], False),
        "nes": SystemInfo("https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Nintendo%20Entertainment%20System%20(Headered)/", ".nes", ['NES'], True),
        "ngp": SystemInfo("https://myrient.erista.me/files/No-Intro/SNK%20-%20NeoGeo%20Pocket/", ".ngp", ['NGP'], True),
        "ngpc": SystemInfo("https://myrient.erista.me/files/No-Intro/SNK%20-%20NeoGeo%20Pocket%20Color/", ".ngc", ['Neo Geo Pocket Color', 'NGPC']),
        "odyssey2": SystemInfo("https://myrient.erista.me/files/No-Intro/Magnavox%20-%20Odyssey%202/", ".bin", ['O2'], True),
        "pc": SystemInfo("https://myrient.erista.me/files/Redump/IBM%20-%20PC%20compatible/", ".cue", ['PC'], True),
        "pc88": SystemInfo("https://myrient.erista.me/files/Internet%20Archive/who_lee/retroachievements_collection_v5/PC-8000-8800/", ".d88", ['PC88'], False),
        #"pc98": SystemInfo("https://myrient.erista.me/files/Redump/NEC%20-%20PC-98%20series/", ".zip", ['PC98']),
        "pcfx": SystemInfo("https://myrient.erista.me/files/TOSEC-ISO/NEC/PC-FX/Games/", ".img", ['PC-FX', 'PCFX'], False),
        #"pokemini": SystemInfo("https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Pokemon%20Mini/", ".zip", ['PMINI']),
        "ps2": SystemInfo("https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation%202/", ".iso", ['PlayStation 2'], False),
        #"ps3": SystemInfo("https://myrient.erista.me/files/No-Intro/Sony%20-%20PlayStation%203%20(PSN)%20(Content)/", "", ['PS3']),
        #"psp": SystemInfo("https://myrient.erista.me/files/TOSEC-ISO/Sony/PlayStation%20Portable/Games/%5BISO%5D/", "", ['PSP Eboots', 'PSP Eboot', 'PlayStation Portable', 'PSP']),
        #"psvita": SystemInfo("https://myrient.erista.me/files/No-Intro/Sony%20-%20PlayStation%20Vita%20(PSN)%20(Content)/", "", ['VITA']),
        #"psx": SystemInfo("https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation/", "", ['PlayStation', 'PSX']),
        #"saturn": SystemInfo("https://myrient.erista.me/files/Redump/Sega%20-%20Saturn/", "", ['SEGA Saturn', 'Saturn', 'SAT']),
        #"sega32x": SystemInfo("https://myrient.erista.me/files/No-Intro/Sega%20-%2032X/", "", ['SEGA 32x', '32X']),
        #"segacd": SystemInfo("https://myrient.erista.me/files/Redump/Sega%20-%20Mega%20CD%20%26%20Sega%20CD/", "", ['SEGA CD', 'SegaCD']),
        #"sg-1000": SystemInfo("https://myrient.erista.me/files/Internet%20Archive/who_lee/retroachievements_collection_v5/SG-1000/", "", ['SG1K']),
        #"supergrafx": SystemInfo("https://myrient.erista.me/files/No-Intro/NEC%20-%20PC%20Engine%20SuperGrafx/", "", ['SGFX']),
        #"snes": SystemInfo("https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Super%20Nintendo%20Entertainment%20System/", ".zip", ['SNES']),
        #"tg16": SystemInfo("https://myrient.erista.me/files/No-Intro/NEC%20-%20PC%20Engine%20-%20TurboGrafx-16/", ".zip", ['TurboGrafx-16', 'TG16']),
        #"tg-cd": SystemInfo("https://myrient.erista.me/files/Redump/NEC%20-%20PC%20Engine%20CD%20&%20TurboGrafx%20CD/", ".zip", ['TurboGrafx-CD', 'TGCD']),
        #"vectrex": SystemInfo("https://myrient.erista.me/files/No-Intro/GCE%20-%20Vectrex/", ""),
        #"vic20": SystemInfo("https://myrient.erista.me/files/No-Intro/Commodore%20-%20VIC-20/", ""),
        #"virtualboy": SystemInfo("https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Virtual%20Boy/", "", ['VB']),
        #"wii": SystemInfo("https://myrient.erista.me/files/Redump/Nintendo%20-%20Wii%20-%20NKit%20RVZ%20[zstd-19-128k]/", "", ['WII']),
        #"windows": SystemInfo("", "", ['Windows', 'PC']),
        #"wonderswan": SystemInfo("https://myrient.erista.me/files/No-Intro/Bandai%20-%20WonderSwan/", "", ['WonderSwan', 'WS']),
        #"wonderswancolor": SystemInfo("https://myrient.erista.me/files/No-Intro/Bandai%20-%20WonderSwan%20Color/", "", ['']),
        #"x68000": SystemInfo("https://myrient.erista.me/files/TOSEC/Sharp/X68000/Games/%5BDIM%5D/", "", ['X68K']),
        #"xbox": SystemInfo("https://myrient.erista.me/files/Redump/Microsoft%20-%20Xbox/", "", ['XBOX']),
        #"xbox360": SystemInfo("https://myrient.erista.me/files/No-Intro/Microsoft%20-%20Xbox%20360%20(Digital)/", "", ['XB360']),
    }

def GetSystemLinkKeyFromSystemName(systemName):
    if systemName in systemLinks:
        return systemName
    for key in systemLinks:
        if systemName in systemLinks[key].emulatorAliases:
            return key
    return None

currentDirectory = os.path.dirname(os.path.abspath(sys.argv[0]))
settingsFilePath = os.path.abspath(os.path.join(currentDirectory, '../../settings/es_settings.xml'))
romsPath = ''
f = open('c:\\temp\\logging.txt', 'a')
f.write('started')
f.write('\n')
f.write('settings file path: ' + settingsFilePath)
f.write('\n')
f.close()
with open(settingsFilePath, "r") as settingsFile:
    lines = settingsFile.readlines()
    for line in lines:
        if line.startswith("<string name=\"ROMDirectory\""):
            romsPath = line.split("\"")[3]
            break
f = open('c:\\temp\\logging.txt', 'a')
f.write('started')
f.write('\n')
f.write('roms path: ' + romsPath)
f.write('\n')
f.close()

for itemToScrape in itemsToScrape:
    folderPath = os.path.abspath(os.path.join(currentDirectory, itemToScrape.directoryPath))
    for filePath in os.listdir(folderPath):
        scrapeFileName = Path(filePath).stem
        scrapeSite = scrapeFileName.split('_')[0]
        with open(filePath, 'r') as fileInfo:
            for line in fileInfo:
                romInfo = line.split('\t')
                url = romInfo[0]
                gameName = romInfo[1]
                systemInfo = romInfo[2].replace("\n", "")
                system = GetSystemLinkKeyFromSystemName(systemInfo)
                if system is None:
                    continue
                systemInfo = systemLinks[system]
                fileToWrite = os.path.join(romsPath, system, gameName + systemInfo.fileType)
                TryWriteRomFile(fileToWrite, scrapeSite, url)

for subdir, dirs, files in os.walk(romsPath):
    if subdir == romsPath:
        continue
    systemName = Path(subdir).name
    systemRomPath = subdir
    dateFormatString = "%Y-%m-%d %H:%M:%S"
    #begin debug lines, delete
    f = open('c:\\temp\\logging.txt', 'a')
    f.write(datetime.now().strftime(dateFormatString))
    f.write('\n')
    f.write(systemName)
    #f.write('\n')
    #f.write(systemFullName)
    f.write('\n')
    f.write(systemRomPath)
    f.write('\n')
    f.write('\n')
    f.close()
    #end debug lines, delete
    
    infoFile = os.path.join(systemRomPath, "RomDownloadInfo.txt")
    nowDateTime = datetime.now()
    if os.path.isfile(infoFile):
        with open(infoFile, "r") as file:
            lines = file.readlines()
            lastUpdatedDateTime = datetime.strptime(lines[0], dateFormatString)
            timeToUpdateThreshold = nowDateTime - timedelta(days=10)
            if (lastUpdatedDateTime >= timeToUpdateThreshold):
                continue
    with open(infoFile, "w") as file:
        file.write(nowDateTime.strftime(dateFormatString))

    systemLink = systemLinks.get(systemName)
    if systemLink is None:
        continue
    time.sleep(1) # don't flood the scraping...
    response = requests.get(systemLink.url)
    htmlData = response.text
    soup = BeautifulSoup(htmlData, "html.parser")
    #allLinks = soup.find_all(name="td", class_="link")
    allTableRows = soup.find_all(name="tr")
    for currentTableRow in allTableRows:
        linkItem = currentTableRow.find(class_="link")
        sizeItem = currentTableRow.find(class_="size")
        dateItem = currentTableRow.find(class_="date")
        if linkItem is None or sizeItem is None or dateItem is None:
            continue
        linkChildItem = linkItem.find(name="a")
        if linkChildItem is None:
            continue
        title = os.path.splitext(linkChildItem.getText())[0]
        hrefValue = linkChildItem['href']
        if hrefValue is None:
            continue
        size = sizeItem.getText()
        if size is None or size == "-":
            continue
        filePath = os.path.join(systemRomPath, title + systemLink.fileType)
        TryWriteRomFile(filePath, 'myrient', systemLink.url + hrefValue)