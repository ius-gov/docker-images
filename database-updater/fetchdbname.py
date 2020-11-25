import argparse
import json
import os
import re
PATTERN = 'Initial\\WCatalog=([a-zA-Z]+)'
def GetDatabaseCatalog(appsettingsFilePath, CannonicalApplicationName):
    normalizedPath = os.path.abspath(appsettingsFilePath)
    with open(normalizedPath) as jsonfile:
        appsettings = json.load(jsonfile)
        connectionString = appsettings['ConnectionStrings'][CannonicalApplicationName]
        return re.split(';', re.split(r'Catalog=', connectionString)[1])[0]

if __name__ == "__main__":
    parser = argparse.ArgumentParser
    parser.add_argument('--appsettingsFilePath',type=str, required=True)
    parser.add_argument('--CannonicalApplicationName', type=str,required=True)
    args = parser.parse_args()
    result = GetDatabaseCatalog(args.appsettingsFilePath,args.CannonicalApplicationName)
    print(result)
    exit(0)
