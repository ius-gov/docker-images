FROM iusdev.azurecr.io/web-build:latest AS pythonbuild

# Nodejs
ENV NODE_VERSION 10.18.0
ENV NODE_DOWNLOAD_SHA 78a46d1e1f6db68c0732981fc9a1fe8583eabb4e232f1ed742f7dedc5bed3ddd

RUN curl -SL "https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-linux-x64.tar.gz" --output nodejs.tar.gz \
    && echo "$NODE_DOWNLOAD_SHA nodejs.tar.gz" | sha256sum -c - \
    && tar -xzf "nodejs.tar.gz" -C /usr/local --strip-components=1 \
    && rm nodejs.tar.gz \
    && ln -s /usr/local/bin/node /usr/local/bin/nodejs

WORKDIR /

COPY . .

RUN wget https://raw.githubusercontent.com/ius-gov/cdn_dupe_checker/master/dupechecker.py -O dupechecker.py
RUN wget https://raw.githubusercontent.com/ius-gov/cdn_dupe_checker/master/requirements.txt -O requirements.txt

RUN pip install -r requirements.txt

RUN npm install
RUN npm install gulp -g
