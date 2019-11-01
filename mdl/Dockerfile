FROM iusdev.azurecr.io/web-build:latest AS pythonbuild
WORKDIR /

COPY . .
RUN apt-get update
RUN apt-get install -y \
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

RUN wget https://raw.githubusercontent.com/ius-gov/cdn_dupe_checker/master/dupechecker.py -O dupechecker.py
RUN wget https://raw.githubusercontent.com/ius-gov/cdn_dupe_checker/master/requirements.txt -O requirements.txt

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
RUN python -m pip install -r requirements.txt


RUN npm install
RUN npm install gulp -g
