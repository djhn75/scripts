#!/bin/bash

FIRSTBASE=$1
LASTBASE=$2
shift 2


for i in $@
do
	EXP=$(sed 's/\.fa.*//' <<< $(basename $i));
	echo "Trim " $NBASES "bp's from " $EXP
	fastx_trimmer -Q33 -f $FIRSTBASE -l $LASTBASE -i $i -o $(dirname $i)"/trimmed/"$EXP".trimmed.fastq" &
done
