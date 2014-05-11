#!/bin/bash

DATA_PATH=$1
TXT_FILES=$DATA_PATH/*;

echo "Romanizing...";
ROMAN_OUT=$DATA_PATH/romanized;
mkdir $ROMAN_OUT;
for f in $TXT_FILES:
	do
		echo "Processing ${f}...";
		romanize_indic_text.py < $f > $ROMAN_OUT/"${f}.romanized";
	done

echo "Extracting Voter Data...";
TMP=$DATA_PATH/tmp;
mkdir $TMP;
DATA_FILES=$ROMAN_OUT/*;
touch $TMP/database.txt;
for f in $DATA_FILES:
	do
		echo "Processing ${f}...";
		python extractVoterDatabase.py $f >> $TMP/database.txt;
	done
 	
