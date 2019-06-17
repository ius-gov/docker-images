FROM mcr.microsoft.com/dotnet/core/sdk:2.1 AS build
# info from https://nodejs.org/dist/v10.15.3/SHASUMS256.txt.asc
ENV NODE_VERSION 10.16.0
#ENV NODE_DOWNLOAD_SHA 6c35b85a7cd4188ab7578354277b2b2ca43eacc864a2a16b3669753ec2369d52
ENV NODE_DOWNLOAD_SHA 2e2cddf805112bd0b5769290bf2d1bc4bdd55ee44327e826fa94c459835a9d9a

RUN curl -SL "https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-linux-x64.tar.gz" --output nodejs.tar.gz \
    && echo "$NODE_DOWNLOAD_SHA nodejs.tar.gz" | sha256sum -c - \
    && tar -xzf "nodejs.tar.gz" -C /usr/local --strip-components=1 \
    && rm nodejs.tar.gz \
    && ln -s /usr/local/bin/node /usr/local/bin/nodejs \
	  && npm -v \
	  && node -v

RUN apt-get update && apt-get install -y \
	git \
	wget \
	curl \
	build-essential \
	zlib1g-dev \
	libncurses5-dev \
	libgdbm-dev \
	libnss3-dev \
	libssl-dev \
	libreadline-dev \
	libffi-dev

# Set Python version
ARG PYTHON_VERSION='3.7.0'
# Set pyenv home
ARG PYENV_HOME=/root/.pyenv

# Install pyenv, then install python versions
RUN git clone --depth 1 https://github.com/pyenv/pyenv.git $PYENV_HOME && \
    rm -rfv $PYENV_HOME/.git

ENV PATH $PYENV_HOME/shims:$PYENV_HOME/bin:$PATH

RUN pyenv install $PYTHON_VERSION
RUN pyenv global $PYTHON_VERSION
RUN pip install --upgrade pip && pyenv rehash

# This version is over 5x fasster than 2.0.4283
RUN npm install -g autorest@2.0.4215

RUN autorest --reset

RUN autorest --version
