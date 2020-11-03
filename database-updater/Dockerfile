FROM iusdev.azurecr.io/sqlpackage-azurecli-base:latest 

ENTRYPOINT echo $AZURE_DEVOPS_TOKEN | az devops login \
    && \
    az artifacts universal download \
        --organization $AZURE_URL \
        --feed $FEED  \
        --name $PROJECT \
        --version $VERSION \
        --path . \
    && ls -la \
    && \
    sqlpackage \
        /Action:Publish \
        /SourceFile:$SOURCEFILE \
        /TargetServerName:$TARGET_SERVER  \
        /TargetDatabaseName:$TARGET_DATABASE  \
        /TargetUser:$DB_USER  \
        /TargetPassword:$DB_PASSWORD  \
        /p:AllowIncompatiblePlatform=true  \
        /p:BlockOnPossibleDataLoss=false  \
        /TargetTimeout:120 

