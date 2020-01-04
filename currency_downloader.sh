#!/bin/sh
aria2c\
    --dir=${HOME}/Data\
    --allow-overwrite\
    --max-connection-per-server=10\
    --split=10\
    --min-split-size=5M\
    --input-file=`dirname $0`/currency_downloader.txt
