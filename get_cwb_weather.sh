#!/bin/sh
TODAY=`date '+%Y-%m-%d'`
DoTime=`date`
projectPath=<PROJECT_PATH>
authorization=<AUTHORIZATION>
mkdir  $projectPath/history

wget -O $projectPath/weather.json "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=${authorization}&locationName=%E8%87%BA%E5%8C%97%E5%B8%82"
cp $projectPath/weather.json  $projectPath/history/${TODAY}.json
