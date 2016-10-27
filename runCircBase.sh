#!/bin/bash
#runCircBase.sh (-p if paired) refGenome chromDir *.fastq


if [ $1 = '-p' ]
then 
	PAIRED=true 
	REFGENOME=$2
	CHROMDIR=$3
	shift
else
	PAIRED=false
	REFGENOME=$1
	CHROMDIR=$2

fi

echo 'Paired = '$PAIRED
echo 'Ref Genome = '$REFGENOME
echo 'ChromDir= '$CHROMDIR

shift
shift
for i in $@
do 
	
	if [ $PAIRED = true ]
	then
		#_S[0-9]+_L[0-9]+_R[1,2]_
		#EXP=$(sed 's/[A-Z]\+_S[0-9]\+_L[0-9]\+_R[1,2]_[0-9]\+.fa.*//' <<< $(basename $i));
		EXP=$(sed 's/_[0-9]\.fa.*//' <<< $(basename $i));
	else
		EXP=$(sed 's/\.fa.*//' <<< $(basename $i));
	fi
	OUTPUT="$(dirname $i)"
	echo "# # # Looking for CircRNAs for -->  --> $EXP "
	

	if [ ! -f circBase/$EXP.bam ]	
	then
		if [ $PAIRED = true ]
			then
			echo "    # MAPPING PAIRED READS #"	
			bowtie2 -p 30 --very-sensitive --mm --score-min=C,-15,0 -x $REFGENOME -1 $OUTPUT/$EXP"*_1*.fa*" -2 $OUTPUT/$EXP"*_2*.fa*" 2> $OUTPUT/circBase/$EXP.log | samtools view -hbuS - | samtools sort - $OUTPUT/circBase/$EXP || { echo "FAILED" ; exit 1 ;}
		
		else
			echo "    # MAPPING SINGLE READS #"	
			bowtie2 -p 30 --very-sensitive --mm --score-min=C,-15,0 -x $REFGENOME -U $i 2> $OUTPUT/circBase/$EXP.log | samtools view -hbuS - | samtools sort - $OUTPUT/circBase/$EXP || { echo "FAILED" ; exit 1 ;}
		fi	
	fi	
	
	if [ ! -f circBase/$EXP"_unmapped.bam" ]
	then
		echo "    # FILTER  UNMAPPED #"
		samtools view -b -hf 4 $OUTPUT/circBase/$EXP".bam"  > $OUTPUT/circBase/$EXP"_unmapped.bam" || { echo "FAILED" ; exit 1 ;}
	fi
	

	if [ ! -f circBase/$EXP"_anchors.fastq" ]
	then	
		echo "    # CREATE ANCHORS #"
		unmapped2anchors.py $OUTPUT/circBase/$EXP"_unmapped.bam" > $OUTPUT/circBase/$EXP"_anchors.fastq" || { echo "FAILED" ; exit 1 ;}
	fi
	

	if [ ! -f circBase/$EXP"_sites.bed" ]
	then
		echo "    # FIND CIRC RNA #"
		bowtie2 -p 30 --reorder --mm --score-min=C,-15,0 -q -x $REFGENOME -U $OUTPUT/circBase/$EXP"_anchors.fastq" | find_circ.py -G $CHROMDIR -p $EXP -s $OUTPUT/circBase/$EXP"_circ.log" > $OUTPUT/circBase/$EXP".bed" 2> $OUTPUT/circBase/$EXP"_sites.bed" || { echo "FAILED" ; exit 1 ;}
	fi
	
	
	echo "### FINISHED for ---> " $EXP
	echo
	echo
done

