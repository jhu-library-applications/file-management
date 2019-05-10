import csv
import os
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--directory', help='the directory of the fileNames to be extracted. optional - if not provided, the script will ask for input')
parser.add_argument('-f', '--fileExtension', help='the file extension of file names to be extracted. optional - if not provided, the script will ask for input')
args = parser.parse_args()

if args.directory:
    directory = args.directory
else:
    directory = input('Enter file path (C:/Test/): ')
if args.fileExtension:
    fileExtension = args.fileExtension
else:
    fileExtension = input('Enter file extension like jpg or txt (no period before extension): ')

directoryName = directory.replace('/', '')
directoryName = directoryName.replace(':', '')
print(directoryName)

startTime = time.time()
f = csv.writer(open(directoryName+'Listing'+'.csv', 'w'))
f.writerow(['currentFilePath']+['fileName']+['newFileName'])
directories = os.walk(directory, topdown=True)
for filePath, subFolders, fileNames in directories:
    for fileName in fileNames:
        if fileName[-3:] == fileExtension:
            print(filePath, fileName)
            f.writerow([filePath]+[fileName])

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))
