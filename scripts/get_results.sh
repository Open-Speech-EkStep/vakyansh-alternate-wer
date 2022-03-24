#!/bin/bash
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <hypothesis.txt> <reference.txt> <output_folder>"
    exit 1
fi

mkdir $3
bin/sclite -h $1 -r $2 -i rm -o sgml -O $3
bin/sclite -h $1 -r $2 -i rm -o all -O $3
bin/sclite -h $1 -r $2 -i rm -o sgml -O $3
bin/sclite -h $1 -r $2 -i rm -o dtl -O $3

