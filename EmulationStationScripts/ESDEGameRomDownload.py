import os.path
import sys
import requests
import zipfile

romPath = sys.argv[1]
gameName = sys.argv[2]
systemName = sys.argv[3]
systemFullName = sys.argv[4]

try:
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
        response = requests.get(url)
        #zipName = os.path.join(os.path.dirname(romPath), "input.zip")
        zipName = romPath + ".zip"
        #os.rename(romPath, zipName)
        if response.status_code == 200:
            with open(zipName, "wb") as file:
                file.write(response.content)
            with zipfile.ZipFile(zipName, 'r') as zipRef:
                zipOutputDirectory = os.path.dirname(romPath)
                zipRef.extractall(zipOutputDirectory)
            os.remove(zipfile)
            #list_of_files = glob.glob('/path/to/folder/*') # * means all if need specific format then *.csv
            #latest_file = max(list_of_files, key=os.path.getctime)
            #os.rename(latest_file, romPath)
            print(f"File '{romPath}' downloaded successfully.")

        else:
            print(f"Failed to download file. Status code: {response.status_code}")
except FileNotFoundError:
    print("Error: The file 'your_file.txt' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")