#!/usr/bin/python


"""
Downloads all fastq files from GSE by a given PRJN accession number PRJNA378265
@author: david John
"""
import argparse, os
from string import split
from subprocess import call

parser = argparse.ArgumentParser(description='Download Fastq files from GSE.')
parser.add_argument('-o', '--output', metavar='N', type=str, help='output file', default="./")
parser.add_argument('-i', '--id', metavar='N', type=str, help='PRJN ID from GEO', required=True)
args = parser.parse_args()



#esearch -db sra -query $GSEID | efetch --format runinfo > $OUTPUT"RunInfo.txt"
#esearch -db sra -query PRJNA378265 | efetch --format runinfo | cut -d ',' -f 1,30 | grep SRR | while read line

IDs=os.popen("esearch -db sra -query PRJNA378265 | efetch --format runinfo | cut -d ',' -f 1,30 | grep SRR").read()
#print IDs
IdDict={}
for line in IDs.split("\n"):
    if line!="":
        line=line.split(",")
        #print line[0] + "   " + line[1]
        if line[1] not in IdDict.keys():
            #print "not in"
            IdDict[line[1]]=[line[0],]
            #print IdDict[line[1]]
        else:
            #print "in"
            value=IdDict[line[1]]
            #print value
            #print line[0]
            #print value.append(line[1])
            IdDict[line[1]].append(line[0])
            #print IdDict[line[1]]
for gsm in IdDict.keys():
    for srr in IdDict[gsm]:
        cmd = "fastq-dump --outdir " + args.output + " " + srr
        #print cmd
        os.popen(cmd)
        cmd = "cat " + args.output + srr +".fastq >> " + args.output + gsm + ".fastq"
        os.popen(cmd)
        #delete SRR files
        #TODO check if file was downloaded completely
        os.popen("rm " + args.output + srr)
        #print cmd
    print "finished for " + args.output + gsm + " joined " + str(IdDict[gsm])
#call(["esearch", "-db", "sra", "-query", args.id, "|", "efetch", "--format", "runinfo", "|", "cut", "-d", "','", "-f", "1,30", "|", "grep", "SRR"])