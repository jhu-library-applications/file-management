import os
import csv
from datetime import datetime
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--directory', help='the directory of the files to be renamed. optional - if not provided, the script will ask for input')
parser.add_argument('-f', '--fileNameCSV', help='the CSV file of name changes. optional - if not provided, the script will ask for input')

args = parser.parse_args()

if args.directory:
    directory = args.directory
else:
    directory = raw_input('Enter the directory of the files that was renamed: ')
if args.fileNameCSV:
    fileNameCSV = args.fileNameCSV
else:
    fileNameCSV = raw_input('Enter the CSV file of renameLog (including \'.csv\'): ')

startTime = time.time()
f=csv.writer(open('renameConfirmation'+datetime.now().strftime('%Y-%m-%d %H.%M.%S')+'.csv','wb'))
f.writerow(['newFileName']+['confirmation']) #This section opens the renamelog csv and checks to make sure all the updated file paths logged in the csv exist in the directory
with open(fileNameCSV) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        updatedFilePath = row['newFileName']
        if os.path.isfile(updatedFilePath) is True:
            confirm = 'changes made'
            f.writerow([updatedFilePath]+[confirm])
        else:
            confirm = 'FILE PATH DOES NOT EXIST'
            f.writerow([updatedFilePath]+[confirm])
f.writerow([]+[])
f.writerow(['currentPaths'] + ['confirmation'])

updateFilePaths = []

with open(fileNameCSV) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        updatedFilePath = row['newFileName']
        updateFilePaths.append(updatedFilePath)


for filePath, subFolders, fileNames in os.walk(directory, topdown=True):
    for fileName in fileNames: #this section checks to see if there are any file paths in the directory that aren't in the renamelog csv
        currentPath = os.path.join(filePath,fileName)
        print currentPath
        if currentPath in updateFilePaths:
            continue
        else:
            confirm = 'not found in renameLog'
            f.writerow([currentPath] + [confirm])

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print 'Total script run time: ', '%d:%02d:%02d' % (h, m, s)
