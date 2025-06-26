import os.path
import sys
import requests
import zipfile
from datetime import datetime
from tqdm import tqdm
import pygetwindow as gw
import os
import time
import math

os.system('title "ESDEGameRomDownload"')

romPath = sys.argv[1]
gameName = sys.argv[2]
systemName = sys.argv[3]
systemFullName = sys.argv[4]

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
        if len(allLines) < 3:
            sys.exit(0)
        host = allLines[0]
        url = allLines[1]
    os.remove(romPath)
    if host == "myrient":
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