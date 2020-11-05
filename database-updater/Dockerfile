FROM iusdev.azurecr.io/sqlpackage-azurecli-base:latest 

COPY . .
RUN chmod +x applydacpac.sh
ENTRYPOINT ./applydacpac.sh
