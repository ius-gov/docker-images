#!/bin/bash

set -e

checkstatus(){

if [ $1 -eq 0 ];then
   echo "[INFO] Successfully Ran the command"
else
   echo "[ERR] Failed to Run Command ,Check the logs to debug the issue"
   exit 1
fi
}
# Doing az devops login to download the artifcat from feed
#Fetching DB name to pass to sql package command.

SERVICE_DATABASE_NAME=`python fetchdbname.py --appsettingsFilePath "/appsettings.idaho.development.json" --CannonicalApplicationName ${SERVICE_NAME}`
checkstatus $?

echo ${PAT_TOKEN} | az devops login
checkstatus $?

az artifacts universal download --organization ${AZURE_URL} --feed ${FEED} --name ${PROJECT} --version ${VERSION} --path /dacpac
checkstatus $?

#Applying Dacpac present to database
echo "Running SQL Package Command"

cd /dacpac/DacPac/
dacpacFilename=`ls | grep -i ".dacpac"`

echo $dacpacFilename
/opt/sqlpackage/sqlpackage /Action:Publish /SourceFile:"/dacpac/DacPac/${dacpacFilename}" /TargetServerName:"${SQL_SERVER_URL},${SQL_SERVER_PORT}" /TargetDatabaseName:"${SERVICE_DATABASE_NAME}" /TargetUser:"${SQL_SERVER_USERNAME}" /TargetPassword:"${SQL_SERVER_PASSWORD}" /p:AllowIncompatiblePlatform=true /p:BlockOnPossibleDataLoss=false /TargetTimeout:120
checkstatus $?
