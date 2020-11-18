#!/bin/bash

# Not installed in this docker image
# sqlcmd -S "${SQL_SERVER_URL},${SQL_SERVER_PORT}" \
# -d "${SERVICE_DATABASE_NAME}" \
# -U "${SQL_SERVER_USERNAME}" \
# -P "${SQL_SERVER_PASSWORD}"

# Doing az devops login to download the artifcat from feed
echo ${PAT_TOKEN} | az devops login

az artifacts universal download \
--organization ${AZURE_URL} \ 
--feed ${FEED} \
--name ${PROJECT} \
--version ${VERSION} \
--path /dacpac
if [ $? -eq 0 ];
then
   echo "[INFO] Successfully logged in with credentials"
elif [ $? -eq 401 ];
then
   echo "[ERR] Unauthorized .Please check the credentials and try again"
exit 1
else
   echo "[INFO] Failed to publish dacpac to sql database,Check the logs to debug the issue"
exit 1
fi 
#Applying Dacpac present to database
echo "Running SQL Package Command"
sqlpackage \
   /Action:Publish \
   /SourceFile:"/dacpac/iUS.${SERVICE_NAME}.Database.SQL.dacpac" \ 
   /TargetServerName:"${SQL_SERVER_URL},${SQL_SERVER_PORT}" \
   /TargetDatabaseName:"${SERVICE_DATABASE_NAME}" \
   /TargetUser:"${SQL_SERVER_USERNAME}" \
   /TargetPassword:"${SQL_SERVER_PASSWORD}" \
   /p:AllowIncompatiblePlatform=true \
   /p:BlockOnPossibleDataLoss=false \
   /TargetTimeout:120

if [ $? -eq 0 ];
   echo "[INFO] Successfully Published dacpac to database"
else
   echo "[ERR] Failed to publish dacpac to sql database,Check the logs to debug the issue"
   exit 1
fi
