FROM mcr.microsoft.com/dotnet/core/sdk:2.1 AS build
# info from https://nodejs.org/dist/v10.15.3/SHASUMS256.txt.asc	
ENV NODE_VERSION 10.15.3	
ENV NODE_DOWNLOAD_SHA 6c35b85a7cd4188ab7578354277b2b2ca43eacc864a2a16b3669753ec2369d52

RUN curl -SL "https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-linux-x64.tar.gz" --output nodejs.tar.gz \	
    && echo "$NODE_DOWNLOAD_SHA nodejs.tar.gz" | sha256sum -c - \	
    && tar -xzf "nodejs.tar.gz" -C /usr/local --strip-components=1 \	
    && rm nodejs.tar.gz \	
    && ln -s /usr/local/bin/node /usr/local/bin/nodejs	
RUN npm install --global typescript@3.1.6