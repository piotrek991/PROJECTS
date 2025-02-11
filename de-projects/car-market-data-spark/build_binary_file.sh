#!/bin/bash

python -m PyInstaller -F /app/app_data/main_extract.py --distpath /app/app_data --name main_extractor
RC=$?

if [ $RC -ne 0 ]
then
  echo "BUILDING A BINARY FILE FAILED"
  exit $RC
fi
exit $RC