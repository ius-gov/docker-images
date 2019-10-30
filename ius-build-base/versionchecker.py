import os
import json
from packaging import version
import re
import sys

def load_banned_versions():
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "bannedversions.json")) as f:
        return json.load(f)

def load_project_assets(project_file):
    print("Loading %s" % project_file)
    with open(project_file) as f:
        return json.load(f)

def check_target_version(target):
    target_array = target.split(',')
    if target_array[0] == '.NETCoreApp':
        m = re.search(r'Version=v(.*)', target_array[1])
        target_version = m.group(1)
        if version.parse(target_version) >= version.parse("2.2"):
            raise ValueError("\tTarget %s is invalid.  We do not support anything greater than or equal to 2.2" % target_version)


def check_dependency(dependency, semversion, banned_versions):
    if dependency in banned_versions:
        banned = banned_versions[dependency]
        banned_semversion = version.parse(banned["Version"])
        if banned["MustBe"] == "LessThan":
            if semversion < banned_semversion:
                return {
                    "message" : "\t\tDependency %s(%s) Passed.  Must be less than %s" % (dependency, semversion, banned["Version"]),
                    "passed" : True
                }
            else:
                return {
                    "message" : "\t\tDependency %s(%s) Failed.  Must be less than %s" % (dependency, semversion, banned["Version"]),
                    "passed" : False
                }
    return {
        "message" : "\t\tDependency %s not banned" % (dependency),
        "passed" : True
    }

def check_package(packageKey, package, banned_versions):
    package_array = packageKey.split("/")
    package_name = package_array[0]
    package_version = package_array[1]
    check_response = check_dependency(package_name, version.parse(package_version), banned_versions)
    error_messages = []
    if check_response["passed"] == False:
        print("\tBanned Version Found in %s (%s)" % (package_name, package_version))
        print(check_response["message"])
        error_messages.append(check_response["message"])
    if "dependencies" in package:
        for dependency in package["dependencies"]:
            print("\tChecking %s" % dependency)
            check_response = check_dependency(dependency, version.parse(package["dependencies"][dependency]), banned_versions)
            if check_response["passed"] == False:
                print("\tBanned Version Found in %s (%s)" % (package_name, package_version))
                print(check_response["message"])
                error_messages.append(check_response["message"])
    
    return error_messages


def find_banned_versions(project_assets, banned_versions):
    if "targets" not in project_assets:
        raise ValueError("Unable to get targets from project assets")
    targets = project_assets["targets"]
    error_messages = []
    for targetKey in targets:
        check_target_version(targetKey)

        for package in targets[targetKey]:
            error_messages = error_messages + check_package(package, targets[targetKey][package], banned_versions)

    return error_messages

def run(project_asset_file):
    banned_versions = load_banned_versions()
    project_assets = load_project_assets(project_asset_file)
    print("Checking for banned versions")
    error_messages = find_banned_versions(project_assets, banned_versions)
    if len(error_messages) > 0:
        print("=====\nBanned Packages Found\n=====")
        exit(1)
    exit(0)

if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        raise ValueError("The first argument of where the project.assets.json is must be provided")
    run(sys.argv[1])
    
    