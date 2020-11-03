FROM mcr.microsoft.com/dotnet/core/runtime:2.1-stretch-slim
RUN apt-get update 
RUN apt-get install -y \
    libunwind8 \
    unzip \ 
    wget 

# Install SQLPackage for Linux and make it executable
RUN wget -progress=bar:force -q -O sqlpackage.zip https://go.microsoft.com/fwlink/?linkid=873926 \
    && unzip -qq sqlpackage.zip -d /opt/sqlpackage \
    && chmod +x /opt/sqlpackage/sqlpackage \
    && rm sqlpackage.zip 
ENV PATH="/opt/sqlpackage/:${PATH}"
#Install Azure CLI for access to universal packages
RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash && apt-get clean up all the garbage leftover

RUN az extension add --name azure-devops
ARG AZURE_URL="https://dev.azure.com/iusdev/"

RUN az devops configure --defaults organization=$AZURE_URL project=Common
ARG AZURE_DEVOPS_TOKEN="TOKEN_MUST_BE_PROVIDED_AT_RUNTIME"
RUN echo $AZURE_DEVOPS_TOKEN | az devops login

ARG FEED="dummyFeed"
#TODO add a build only name with a 0.0.0 version 
ARG PROJECT="DummyProject" 
ARG VERSION="0.1.0"

# the first time you run this command it takes about 45 seconds to install the tool.  Do it in build rather than when we apply the database
RUN az artifacts universal download \
  --organization $AZURE_URL \
  --feed $FEED  \
  --name $PROJECT \
  --version $VERSION \
  --path . \
  && rm iUS* \
  && az devops logout