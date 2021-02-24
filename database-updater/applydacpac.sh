#!/bin/bash
set -e
if [ "$DEBUG_TRUE" == "True"]
then
  set -x
fi

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

SERVICE_DATABASE_NAME=`python fetchdbname.py --appsettingsFilePath "/app/appsettings/appsettings.${ClientStateName}.development.json" --CannonicalApplicationName ${SERVICE_NAME}`
checkstatus $?

echo ${PAT_TOKEN} | az devops login
checkstatus $?

ARTIFACT_VERSION=`echo $VERSION | cut -d "." -f2-`
az artifacts universal download --organization ${AZURE_URL} --feed ${FEED} --name ${PROJECT}.dacpac-artifact --version ${ARTIFACT_VERSION} --path /dacpac
checkstatus $?

#Applying Dacpac present to database
echo "Running SQL Package Command"

cd /dacpac/
foldername=$(ls)
cd /dacpac/${foldername}/
dacpacFilename=`ls | grep -i ".dacpac"`
folderpath=$(pwd)

DACPACGUID=$(uuidgen)

echo $dacpacFilename
/opt/sqlpackage/sqlpackage /Action:Publish /SourceFile:"$folderpath/$dacpacFilename" /TargetServerName:"${SQL_SERVER_URL},${SQL_SERVER_PORT}" /TargetDatabaseName:"${SERVICE_DATABASE_NAME}" /TargetUser:"${SQL_USERNAME}" /TargetPassword:"${SQL_PASSWORD}" /p:AllowIncompatiblePlatform=true /p:BlockOnPossibleDataLoss=false /TargetTimeout:120 | seqcli ingest -a GR7BMA8ZiVATLskgQGq6 -p ServiceName=${SERVICE_NAME} -p ArtifactVersion=${ARTIFACT_VERSION} -p DacpacGuid=$DACPACGUID
checkstatus $?
