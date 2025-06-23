import os.path
import sys
from datetime import datetime

f = open('c:\\temp\\logging.txt', 'a')
f.write(datetime.now().strftime("%Y-%m-%d"))
f.write('\n')
f.write("app started up")
f.write('\n')
f.write('\n')
f.close()