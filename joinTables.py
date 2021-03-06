#!/usr/bin/python
'''
this script merges all the given files on an specific column
Created on Apr 16, 2013


TableA:
        A a 1 2 3 4
        B b 2 3 4 5
        C c 3 4 5 6

TableB:
        C c 0,3 0,4 0,5
        D d 0,4 0,5 0,6
        E d 0,5 0,6 0,7
        F d 0,6 0,7 0,8

ResultTable of "joinTables -f Table1.txt Table2.txt -k 1 2 -c 3 4 5"
        A a 1 2 3 4 -- -- --
        B b 2 3 4 5 -- -- --
        C c 3 4 5 6 0,3 0,4 0,5
        D  d -- -- -- 0,4 0,5 0,6
        E  d -- -- -- 0,5 0,6 0,7
        F d  -- -- --0,6 0,7 0,8

@author: david John
'''
import argparse, os
from string import split

parser = argparse.ArgumentParser(description='Merge tables.')
parser.add_argument('-f', '--files', metavar='N', type=str, nargs='+', help='the list of files', required=True)
parser.add_argument('-t', '--top', metavar='N', type=str, nargs="+", help='list of header names (space separated)')
parser.add_argument('-c', '--columns', metavar='N', type=int, nargs='+', help='columns to keep (space separated)',
                    default=[2], )
parser.add_argument('-k', '--keys', metavar='N', nargs='+', type=int, help='columnnumber on which to join', default=[1])
parser.add_argument('-d', '--delimiter', metavar='N', type=str, help='delimiter', default="\t")
parser.add_argument('-e', '--empty', metavar='N', type=str, help='Sign for empty Values', default="--")
args = parser.parse_args()

idDict = {}
if args.top == None:
    header = []
    for file in args.files:
        header.append(os.path.basename(file))

else:
    header = args.top

fileNumber = len(args.files)
fileCounter = 0
keySet = ()

for file in args.files:  # loop through all files
    file = open(file)

    for line in file:  # loop through current file
        line = line.split()
        keyTuple = ()
        for k in args.keys:
            keyTuple = keyTuple + (line[k],)

        value = []
        for column in args.columns:  # get the needed values
            try:
                value.append(line[column])
            except IndexError:
                raise ValueError("Not enough rows in line: %s in file %s" % (" ".join(line), file.name))

        if keyTuple in keySet:
            # currentDefaultList=idDict[keyTuple]
            # currentDefaultList[fileCounter]=value
            # idDict[keyTuple]=currentDefaultList
            idDict[keyTuple][fileCounter] = value  # replace filecounter List with values from current File
        else:
            currentDefaultList = [["--"] * len(args.columns)] * len(
                args.files)  # create default list, with all values empty
            currentDefaultList[fileCounter] = value
            idDict[keyTuple] = currentDefaultList
            keySet = keySet + (keyTuple,)

    fileCounter += 1
deli = "\t" * len(args.columns)
print "\t" * len(args.keys), deli.join(header)
for keyTuple in keySet:
    output = list(keyTuple)
    for v in idDict[keyTuple]:
        output = output + v
    print "\t".join(output)