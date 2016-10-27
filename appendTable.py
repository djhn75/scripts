#!/usr/bin/python

'''
this script adds specific columns to a table
Created on Okt 2016

@author: David John
'''
import argparse
from string import split

parser = argparse.ArgumentParser(description='Add a specific colums to the end of a file')
parser.add_argument('-t1', '--table1', metavar='file', type=str, help='original list to add colums',required=True)
parser.add_argument('-t2', '--table2', metavar='file', type=str, help='list with values to append', required=True)
parser.add_argument('-k1', '--key1', metavar='int', type=int, help='key from the table1', default=0)
parser.add_argument('-k2', '--key2', metavar='int', type=int, help='key from the table2', default=0)
parser.add_argument('-c1', '--column1', metavar='int', type=int, help='columns to keep from table1', default=1)
parser.add_argument('-c2', '--column2', metavar='int', type=int, help='columns to keep from table2', default=1)
parser.add_argument('-d', '--delimiter', metavar='str', type=str, help='delimiter of gene list', default="\t")
args = parser.parse_args()

table1 = open(args.mirna)
table2 = open(args.geneList)
d = args.delimiter
k1 = args.key1
k2 = args.key2


# extract miRNAs from miranda database
miRnaDict = {}  # GeneId:biotype
geneNameDict = {}
for line in miRnaDb:
    info = line.split("\t")
    # start=
    geneId = info[3].replace("\"", "")
    miRnaId = info[1].replace("\"", "")

    if geneId in miRnaDict:
        if not miRnaId in miRnaDict[geneId]:
            miRnaDict[geneId] = miRnaDict[geneId] + "," + miRnaId
    else:
        miRnaDict[geneId] = miRnaId

# add bioTypes to geneList
for line in geneList:
    line = line.rstrip()
    line = line.split(d)
    geneId = line[k].replace("\"", "")
    if "," in geneId:
        geneId = geneId.split(",")[0]
    if geneId in miRnaDict:
        line.append(miRnaDict[geneId])
    else:
        line.append("--")
    print "\t".join(line)
