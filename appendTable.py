#!/usr/bin/python

'''
this script adds specific columns to a table
Created on Okt 2016

@author: David John
'''
import argparse
from string import split

parser = argparse.ArgumentParser(description='Add a specific colums to the end of a file')
parser.add_argument('-t1', '--table1', metavar='file',  type=str, help='original list to add colums',required=True)
parser.add_argument('-t2', '--table2', metavar='file', type=str, help='list with values to append', required=True)
parser.add_argument('-k1', '--keys1', metavar='int', nargs='+', type=int, help='keys from the table1 (0-based)', default=[0])
parser.add_argument('-k2', '--keys2', metavar='int', nargs='+', type=int, help='keys from the table2  (0-based)', default=[0])
parser.add_argument('-c1', '--columns1', metavar='int', nargs='+', type=int, help='columns to keep from table1  (0-based)', default=[1])
parser.add_argument('-c2', '--columns2', metavar='int', nargs='+', type=int, help='columns to keep from table2  (0-based)', default=[1])
parser.add_argument('-d', '--delimiter', metavar='str', type=str, help='delimiter of gene list', default="\t")
args = parser.parse_args()

table1 = open(args.table1)
table2 = open(args.table2)
d = args.delimiter
keys1 = args.keys1
keys2 = args.keys2
columns1 = args.columns1
columns2 = args.columns2

# extract miRNAs from miranda database
table2Dict = {}  # key1:columns1

for line in table2:
    line = line.rstrip().split(d)
    # start=

    # assemble keyTuple
    keyTuple = ()
    for key in keys2:
        keyTuple=keyTuple + (line[key],)

    # assemble columnTuple
    columnList=[]
    for column in columns2:
        columnList.append(line[column])

    #combine key with column
    if keyTuple in table2Dict:
        assert len(table2Dict[keyTuple]) == len(columnList)
        temp=[]
        for column,tableColumn in zip(columnList,table2Dict[keyTuple]):
            if column not in tableColumn:
                temp.append(tableColumn + ", " + column)
            else:
                temp.append(tableColumn)
        table2Dict[keyTuple] = temp
    else:
        table2Dict[keyTuple] = columnList

# add bioTypes to geneList
for line in table1:
    line = line.rstrip()
    line = line.split(d)

    keyTuple = ()
    for key in keys1:
        keyTuple = keyTuple + (line[key],)


    columnList = []
    for column in columns1:
        columnList.append(line[column])


    output=[]
    for key in keyTuple:
        output.append(key)
    for column in columnList:
        output.append(column)
    if keyTuple in table2Dict.keys():
        for column in table2Dict[keyTuple]:
            output.append(column)
    else:
        output += ["--"]*len(column2)
    """
    if "," in geneId:
        geneId = geneId.split(",")[0]
    if geneId in miRnaDict:
        line.append(miRnaDict[geneId])
    else:
        line.append("--")
    """
    print "\t".join(output)
