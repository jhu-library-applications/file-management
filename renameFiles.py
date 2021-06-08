import os
import time
from datetime import datetime
import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--filename', help='the CSV file of name changes.')
parser.add_argument('-m', '--makeChanges', help='Enter "true" if script \
                    should actually rename files. Oherwise, it only \
                    creates a log of the expected file name changes')
args = parser.parse_args()

if args.filename:
    filename = args.filename
else:
    filename = input('Enter the CSV file of name changes: ')
if args.makeChanges:
    makeChanges = args.makeChanges
else:
    makeChanges = input('Enter "true" for script to actually rename files')

startTime = time.time()

df = pd.read_csv(filename)

logList = []
for count, row in df.iterrows():
    row = row
    dir = row['fileLocation']
    file = row['file']
    newFilename = row['newFile']
    oldPath = os.path.join(dir, file)
    row['oldPath'] = oldPath
    newPath = os.path.join(dir, newFilename)
    row['newPath'] = newPath
    if makeChanges == 'true':
        os.rename(oldPath, newPath)
        row['changed'] = 'True'
    else:
        print('log of expected file name changes created - no files renamed')
        row['changed'] = 'False'
    logList.append(row)

log = pd.DataFrame.from_dict(logList)
print(log.head(15))
dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
log.to_csv('logOfEditingMetadataByItemID_'+dt+'.csv', index=False)

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))
