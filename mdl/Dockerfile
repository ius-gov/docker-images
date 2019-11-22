FROM iusdev.azurecr.io/web-build:latest AS pythonbuild
WORKDIR /

COPY . .

RUN wget https://raw.githubusercontent.com/ius-gov/cdn_dupe_checker/master/dupechecker.py -O dupechecker.py
RUN wget https://raw.githubusercontent.com/ius-gov/cdn_dupe_checker/master/requirements.txt -O requirements.txt

RUN npm install
RUN npm install gulp -g
