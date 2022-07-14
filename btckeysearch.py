#!/usr/bin/env python3

import os
import argparse
import re

# intro
print('\n*=*=*= BTC Key Search =*=*=*\n')
print('This tool scans through all the files in a given directory (including subdirectories)')
print('searching for strings that could be private keys.')
print('To run it use the -d option and provide the directory you want to scan.')
print('example: btckeysearch.py /home/user/dir\n\n')

parser = argparse.ArgumentParser(description='Bitcoin private key finder')
parser.add_argument('-d', metavar='directory', type=str,
                    required=True, help='Directory to scan')
args = parser.parse_args()
directory = args.d


def getListOfFiles(dirName):
    # create a list of file and sub directories
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
    return allFiles


# Get the list of all files in the fiven path
listOfFiles = getListOfFiles(directory)

# Changes working directory to avoid issues with file opening
os.chdir(directory)

n_files = len(listOfFiles)
print(f'there are {n_files} to scan')
i = 0
# iterate through all the files
while i < n_files:
    f = open(listOfFiles[i], 'r')
#    filetext = f.read()
#    f.close()
    prog = 1
# iterate through the lines in the current file
    while True:
        line = f.readline()
        if not line:
            break
# regex for Bitcoin private keys
        matches = re.findall(r'[5KL][1-9A-HJ-NP-Za-km-z]{50,51}$', line)
        if matches != [] and prog == 1:
            print(f'\n======== Matches in {listOfFiles[i]} ========')
        if matches != []:
            print(f'{prog}:  {matches}')
            prog += 1
    f.close()
    i += 1
