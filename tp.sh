#!/bin/bash

PRINTMAT=0
PRINTIME=0

while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -a|--algo)
    ALGO="$2"
    shift # past argument
    shift # past value
    ;;
    -e1|--path1)
    PATH1="$2"
    shift # past argument
    shift # past value
    ;;
    -e2|--path2)
    PATH2="$2"
    shift # past argument
    shift # past value
    ;;
    -p|--printMat)
    PRINTMAT=1
    shift # past argument
    ;;
    -t|--printTime)
    PRINTIME=1
    shift # past argument
    ;;
esac
done

python main.py ${ALGO} ${PATH1} ${PATH2} ${PRINTMAT} ${PRINTIME}

