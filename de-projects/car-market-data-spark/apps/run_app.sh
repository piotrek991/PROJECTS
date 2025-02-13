#!/bin/bash

/opt/spark/apps_ext/main_extractor -d /opt/spark/data
spark-submit \
  --master spark://spark-master:7077 \
  --deploy-mode client \
  /opt/spark/apps/prepare_time_charts.py

RC=$?
if [ $RC -ne 0 ]
then
  echo "during process of data analysis problem occured"
  exit 1
fi
exit 0