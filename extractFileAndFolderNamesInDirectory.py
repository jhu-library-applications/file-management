import csv
import os
import time
from datetime import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--filePath', help='File path (C:/Test/)')
parser.add_argument('-f', '--fileExtension', help='File extensions')
args = parser.parse_args()

if args.filePath:
    filePath = args.filePath
else:
    filePath = input('Enter file path (C:/Test/): ')
if args.fileExtension:
    fileExtension = args.fileExtension
else:
    fileExtension = input('Enter file extension like jpg or txt (no period): ')

dt = datetime.now().strftime('%Y-%m-%d%H.%M.%S')
startTime = time.time()
f = csv.writer(open('filesAndFoldersListing_'+dt+'.csv', 'w'))
f.writerow(['currentFilePath']+['fileName'])
directories = os.walk(filePath, topdown=True)
for root, dirs, files in directories:
    for filename in files:
        print(filename)
        if filename[-3:] == fileExtension:
            print(filePath, filename)
            f.writerow([filePath]+[filename])

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))
