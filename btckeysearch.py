#!/usr/bin/env python3

import os
import argparse
import re


class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


# intro
print(color.YELLOW + '\n*=*=*= BTC Key Search =*=*=*\n' + color.END)
print('This tool scans through all the files in a given directory (including subdirectories)')
print('searching for strings that could be private keys.')
print('To run it use the -d option and provide the directory you want to scan.\n')
print(color.RED + 'example:' + color.END + ' btckeysearch.py -d /home/user/dir\n')

parser = argparse.ArgumentParser(description='Cryptocurrency private key finder')
parser.add_argument('-d', metavar='directory', type=str, required=True, help='Directory to scan')
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
print(color.GREEN + f'There are {n_files} files to scan' + color.END)
i = 0
matches = []    # bitcoin private keys
matchexp = []   # xpriv keys
matchex = []    # monero private spend key
# iterate through all the files
while i < n_files:
    f = open(listOfFiles[i], 'r')
    prog = 1
# iterate through the lines in the current file
    while True:
        line = f.readline()
        if not line:
            break
# regex for Bitcoin private keys
        res = re.findall(r'[5KL][1-9A-HJ-NP-Za-km-z]{50,51}$', line)
        if res:
            matches.append(res)
# regex for xpriv keys
        res2 = re.findall(r'\bxprv[a-km-zA-HJ-NP-Z1-9]{107,108}\b', line)
        if res2:
            matchexp.append(res2)
# regex for xmr private spend keys
        res3 = re.findall(r'\b[0-9a-fA-F]{62}[0][0-9a-fA-F]\b', line)
        if res3:
            matchex.append(res3)
    f.close()
# print matches in the current file
# bitcoin private keys
    if len(matches) > 0:
        prog = 0
        print(color.DARKCYAN + f'\n======== Bitcoin private keys in {listOfFiles[i]} ========' + color.END)
        nk = len(matches)
        iw = 0
        while iw < nk:
            if matches[iw]:
                prog += 1
                print(f'{prog}: {matches[iw]}')
            iw += 1
        matches = []
# xpriv keys
    if len(matchexp) > 0:
        prog2 = 0
        print(color.DARKCYAN + f'\n======== BIP32 rootkeys in {listOfFiles[i]} ========' + color.END)
        nk2 = len(matchexp)
        iw2 = 0
        while iw2 < nk2:
            if matchexp[iw2]:
                prog2 += 1
                print(f'{prog2}: {matchexp[iw2]}')
            iw2 += 1
        matchexp = []
# monero private spend key
    if len(matchex) > 0:
        print(color.DARKCYAN + f'\n======== Monero private spend keys in {listOfFiles[i]} ========' + color.END)
        nk3 = len(matchex)
        iw3 = 0
        prog3 = 0
        while iw3 < nk3:
            if matchex[iw3]:
                prog3 += 1
                print(f'{prog3}: {matchex[iw3]}')
            iw3 += 1
        matchex = []
# go to next file
    i += 1
