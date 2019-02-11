import os
import csv
from datetime import datetime
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--directory', help='the directory of the files to be renamed. optional - if not provided, the script will ask for input')
parser.add_argument('-f', '--fileNameCSV', help='the CSV file of name changes. optional - if not provided, the script will ask for input')
parser.add_argument('-m', '--makeChanges', help='Enter "true" to if the script should actually rename the files (otherwise, it will only create a log of the expected file name changes). optional - if not provided, the script will to "false"')
args = parser.parse_args()

if args.directory:
    directory = args.directory
else:
    directory = raw_input('Enter the directory of the files to be renamed: ')
if args.fileNameCSV:
    fileNameCSV = args.fileNameCSV
else:
    fileNameCSV = raw_input('Enter the CSV file of name changes (including \'.csv\'): ')
if args.makeChanges:
    makeChanges = args.makeChanges
else:
    makeChanges = raw_input('Enter "true" to if the script should actually rename the files (otherwise, it will only create a log of the expected file name changes): ')

directoryName = directory.replace('/', '')
directoryName = directoryName.replace(':', '')
print directoryName

startTime = time.time()
f=csv.writer(open('renameLog'+directoryName+datetime.now().strftime('%Y-%m-%d %H.%M.%S')+'.csv','wb'))
f.writerow(['oldFileName']+['newFileName'])
for filePath, subFolders, fileNames in os.walk(directory, topdown=True):
    for fileName in fileNames:
        with open(fileNameCSV) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                oldFileName = row['fileName']
                newFileName = row['newFileName']
                currentFolderName = row['currentFilePath']
                if fileName == oldFileName and filePath == currentFolderName:
                    oldPath = os.path.join(filePath,fileName)
                    newPath = os.path.join(filePath,newFileName)
                    print 'anticipated changes: '+oldPath+', '+newPath
                    f.writerow([oldPath]+[newPath])
                    if makeChanges == 'true':
                        if os.path.exists(newPath):
                            print "Error renaming '%s' to '%s': destination file already exists." % (oldPath, newPath)
                        else:
                            os.rename(oldPath,newPath)
                    else:
                        print 'log of expected file name changes created only, no files renamed'

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print 'Total script run time: ', '%d:%02d:%02d' % (h, m, s)
