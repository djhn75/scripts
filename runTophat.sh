#!/bin/bash
#runTophat.sh S*


REFGENOME=$1
shift
for i in $@
do 
	EXPNAME=$(sed 's/_[1,2].trimmed.fastq//' <<< $(basename $i));
	echo "tophat2 --no-coverage-search -p 4 -o" $(dirname $i)"/tophat/"$EXPNAME $REFGENOME $EXPNAME"_1.fastq.trimmed.fastq" $EXPNAME"_2.fastq.trimmed.fastq"
	tophat2 --no-coverage-search -p 4 -o $(dirname $i)"/tophat/"$EXPNAME $REFGENOME $EXPNAME"_1.trimmed.fastq" $EXPNAME"_2.trimmed.fastq" 
done
