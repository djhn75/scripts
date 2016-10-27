#!/usr/bin/python
'''
this script merges the barcodes form raw illumina Data with with the sequencing reads
Created on Apr 16, 2013

@author: david
'''
import argparse,sys, os
from string import split, replace, ascii_letters, rfind


def handleSingleEnd(barcodeRow,readRow,convertQual, outFile):
    global keepNumber
    global discardNumber
    
    barcodeLine = barcodeRow.rstrip().split("\t")
    
    if barcodeLine[10] == "1":  #check if barcode passes Illumina filter
        barcodeSeq,barcodeQual=barcodeRow.split("\t")[8:10]
        #print barcodeSeq,barcodeQual
        
        readArray=readRow.split("\t")
        
        if readArray[10] == "1":    #check if barcode passes Illumina filter
            barcodeKey = barcodeLine[0]+ ":" + ":".join(barcodeLine[2:6]) + ":#" + barcodeLine[6]
            readKey = readArray[0]+ ":" + ":".join(readArray[2:6]) + ":#" + readArray[6]
            
            if barcodeKey == readKey:
                ID=readArray[0]+ ":" + ":".join(readArray[2:6]) + ":#" + readArray[6] + "/" + readArray[7]
                seq=barcodeSeq+readArray[8]
                qual=barcodeQual+readArray[9]
                
                #skip sequences that contain an unknown base
                if "." in seq: 
                    #print >> sys.stderr,"read contained unkwon base"
                    discardNumber+=1
                    return
                #replace dots with N in seq      
                #seq=seq.replace(".","N")
                
                if convertQual:
                    a=[]
                    for qualChar in qual:
                        phredQual=ord(qualChar)-64
                        phredChar=chr(phredQual+33)
                        a.append(phredChar)
                    qual="".join(a)
                
                keepNumber+=1
                print >> outFile, "@"+ID
                print >> outFile, seq
                print >> outFile, "+"
                print >> outFile, qual
            else:
                print >> sys.stderr,"barcodeKey and readKey dont fit (" + barcodeKey +" | "+ readKey + ")"
                discardNumber+=1
        else:
            #print >> sys.stderr,"read did not pass illumina quality filter " + readArray[10]
            discardNumber+=1
    else:
        #print >> sys.stderr,"read did not pass illumina quality filter " + barcodeLine[10]
        discardNumber+=1
    

def handlePairedEnd(barcodeRow,readRow1,readRow2,convertQual, outFile1, outFile2):
    global keepNumber
    global discardNumber
    
    barcodeLine = barcodeRow.rstrip().split("\t")
    
    if barcodeLine[10] == "1":  #check if barcode passes Illumina filter
        barcodeSeq,barcodeQual=barcodeRow.split("\t")[8:10]
        #print barcodeSeq,barcodeQual
        
        readArray1=readRow1.split("\t")
        readArray2=readRow2.split("\t")
        
        if readArray1[10] == "1" and readArray2[10] == "1":    #check if barcode passes Illumina filter
            barcodeKey = barcodeLine[0]+ ":" + ":".join(barcodeLine[2:6]) + ":#" + barcodeLine[6]
            
            #check if both read Keys are equal
            readKey1 = readArray1[0]+ ":" + ":".join(readArray1[2:6]) + ":#" + readArray1[6]
            readKey2 = readArray2[0]+ ":" + ":".join(readArray2[2:6]) + ":#" + readArray2[6]
            
            if readKey1 != readKey2:
                print >> sys.stderr,"readKey1 and readKey2 dont fit (" + readKey1 +" | "+ readKey2 + ")"
                #exit(0)
                
            readKey = readKey1
            
            if barcodeKey == readKey:
                ID=readArray1[0]+ ":" + ":".join(readArray1[2:6]) + ":#" + readArray1[6] + "/" + readArray1[7]
                seq1=barcodeSeq+readArray1[8]
                qual1=barcodeQual+readArray1[9]
                
                seq2=barcodeSeq+readArray2[8]
                qual2=barcodeQual+readArray2[9]
                #skip sequences that contain an unknown base
                if "." in seq1 or "." in seq2 : 
                    #print >> sys.stderr,"read contained unkwon base " + seq1 + "\t" + seq2
                    discardNumber+=1
                    return
                #replace dots with N in seq      
                #seq=seq.replace(".","N")
                
                if convertQual:
                    a=[]
                    for qualChar in qual1:
                        phredQual=ord(qualChar)-64
                        phredChar=chr(phredQual+33)
                        a.append(phredChar)
                    qual1="".join(a)
                    
                    a=[]
                    for qualChar in qual2:
                        phredQual=ord(qualChar)-64
                        phredChar=chr(phredQual+33)
                        a.append(phredChar)
                    qual2="".join(a)
                
                keepNumber+=1
                print >> outFile1, "@"+ID
                print >> outFile1, seq1
                print >> outFile1, "+"
                print >> outFile1, qual1
                
                print >> outFile2, "@"+ID
                print >> outFile2, seq2
                print >> outFile2, "+"
                print >> outFile2, qual2
            else:
                print >> sys.stderr,"barcodeKey and readKey dont fit (" + barcodeKey +" | "+ readKey + ")"
                discardNumber+=1
        else:
            #print >> sys.stderr,"reads did not pass illumina quality filter " + readArray1[10] + " " + readArray2[10]
            discardNumber+=1
    else:
        #print >> sys.stderr,"barcode did not pass illumina quality filter " + barcodeLine[10]
        discardNumber+=1

parser = argparse.ArgumentParser(description='Merge barcode with illumina reads and convert to fastQ format.')
parser.add_argument('-b', '--barcodes', metavar='N', type=str, nargs='+', help='the list of barcode files', required=True)
parser.add_argument('-r', '--reads', metavar='N', type=str, nargs='+', help='the list of sequence read files', required=True)
parser.add_argument('-o', '--outFile', metavar='N', type=str, help='outFile Prefix', required=True)
parser.add_argument('-r2', '--reads2', metavar='N', type=str, nargs='+', help='the list of sequence read files (paired-end)')
parser.add_argument("-c", "--convertQual", help="convert Phred+64 to Phred+32", action="store_true")
parser.add_argument("-v", "--verbose", help="show what is going on", action="store_true", default=False)

args = parser.parse_args()
#parser.print_help()

#check if sequencing was paired end
paired= True if args.reads2 else False
convertQual= True if args.convertQual else False

#create outFile directory if necessarry
prefix=args.outFile

path=prefix[:prefix.rfind("/")+1] if "/" in prefix else ""
if not os.path.exists(path) and path!="":
    os.makedirs(path)
    
outFilePrefix= prefix[prefix.rfind("/")+1:]

print path
print outFilePrefix
if outFilePrefix.endswith("fastq"):
    outFilePrefix= outFilePrefix[:outFilePrefix.rfind(".fastq")]

#check if the number of files is the same for all input lists
if paired:
    if len(args.barcodes) != len(args.reads) or len(args.reads) != len(args.reads2):
        print  >> sys.stderr,"ERROR: unequal Number of Files!! Check your Input (Paired-end)"
        sys.exit(1)
    outFile1 = open(path+outFilePrefix+"_1.fastq", "w")
    outFile2 = open(path+outFilePrefix+"_2.fastq", "w")
    
    print  >> sys.stderr,"create File1: " + outFile1.name
    print  >> sys.stderr,"create File2: " + outFile2.name
else:
    if len(args.barcodes) != len(args.reads):
        print  >> sys.stderr,"ERROR: unequal Number of Files!! Check your Input"
        sys.exit(1)
    outFile = open(path+outFilePrefix+".fastq","w")    
    print  >> sys.stderr,"create File1: " + outFile.name



i=0
discardNumber=0
keepNumber=0

for barcode in args.barcodes:
    if args.verbose:
        print  >> sys.stderr,"merging: "+ barcode[barcode.rfind("/")+1:]
    barcodeFile=open(barcode)
    readFile=open(args.reads[i])
    
    #read right sequence
    if paired:
        readFile2=open(args.reads2[i])
        
    #print barcode + " " + args.reads[i]
    
    for barcodeRow in barcodeFile:
        readRow1=readFile.readline().rstrip()
        if(readRow1==""): 
                print "ERROR:EOF of readFile!!! Filegroups may have unequal line numbers"
                exit(0)
                
        if paired:
            readRow2=readFile2.readline().rstrip()
            if(readRow2==""): 
                print "ERROR:EOF of readFile2!!! Filegroups may have unequal line numbers"
                exit(0)
            
            handlePairedEnd(barcodeRow, readRow1, readRow2, convertQual, outFile1, outFile2)
        else:
            handleSingleEnd(barcodeRow, readRow1, convertQual, outFile)
        
    
    i=i+1
print  >> sys.stderr,"discarded: "+ str(discardNumber) +" reads"
print  >> sys.stderr,"keep: " + str(keepNumber) + " reads"
print  >> sys.stderr,"Total: " + str(keepNumber + discardNumber)
