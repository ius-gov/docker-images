FROM iusdev.azurecr.io/sqlpackage-azurecli-base:latest 
RUN apt-get update && apt-get install -y python-dev build-essential python-pip
COPY applydacpac.sh /applydacpac.sh
COPY fetchdbname.py /fetchdbname.py
RUN chmod +x applydacpac.sh
ENTRYPOINT ./applydacpac.sh
