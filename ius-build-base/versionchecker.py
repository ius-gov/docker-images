import os
import json
from packaging import version
import re
import argparse
import logging


class VersionCheckResult:
    def __init__(self):
        self.passed = False
        self.faults = []


class Fault:
    def __init__(self, dependency, version, message):
        self.dependency = dependency
        self.version = version
        self.message = message


class VersionChecker:
    def __init__(self, log_level, project_assets_location, allowed_ius_state_codes):
        self.log_level = log_level
        self.project_assets_location = project_assets_location
        self.allowed_ius_state_codes = allowed_ius_state_codes

        logging.basicConfig(level=log_level, format='%(asctime)-15s [%(levelname)s] %(message)s')
        self.logger = logging.getLogger("VersionChecker")
        self.banned_versions = None
        self.project_assets = None

    def load_banned_versions(self):
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "bannedversions.json")) as f:
            self.banned_versions = json.load(f)

    def load_project_assets(self):
        self.logger.log(logging.INFO, "Loading %s" % self.project_assets_location)
        with open(self.project_assets_location) as f:
            self.project_assets = json.load(f)

    #
    # Check the target version of the app.
    def check_target_version(self, target):
        target_array = target.split(',')
        if target_array[0] == '.NETCoreApp':
            m = re.search(r'Version=v(.*)', target_array[1])
            target_version = m.group(1)
            # At this point, we only allow versions 2.1
            if version.parse(target_version) >= version.parse("2.2"):
                raise ValueError(
                    "\tTarget %s is invalid.  We do not support anything greater than or equal to 2.2" % target_version)

    def check_ius_dependency(self, dependency, semversion) -> Fault:
        if dependency.startswith("iUS"):
            major_version = semversion.release[0]
            if major_version not in self.allowed_ius_state_codes:
                return Fault(dependency, semversion,
                             "Dependency %s(%s) Failed.  It is not in the allowed state codes (%s)" %
                             (dependency, semversion, self.allowed_ius_state_codes))
        return None

    def check_banned_dependency(self, dependency, semversion) -> Fault:
        if dependency in self.banned_versions:
            banned = self.banned_versions[dependency]
            banned_semversion = version.parse(banned["Version"])
            if banned["MustBe"] == "LessThan":
                if semversion < banned_semversion:
                    self.logger.log(logging.DEBUG, "Dependency %s(%s) Passed.  Must be less than %s" % (
                        dependency, semversion, banned["Version"]))
                    return None
                else:
                    return Fault(dependency, semversion, "Dependency %s(%s) Failed.  Must be less than %s" % (
                        dependency, semversion, banned["Version"]))

        self.logger.log(logging.DEBUG, "Dependency %s not banned" % dependency)
        return None

    def check_package(self, package_key, package) -> []:
        package_array = package_key.split("/")
        package_name = package_array[0]
        package_version = version.parse(package_array[1])

        check_response = self.check_banned_dependency(package_name, package_version)
        faults = []
        if check_response:
            self.logger.log(logging.WARNING, "\tBanned Version Found in %s (%s)" % (package_name, package_version))
            self.logger.log(logging.WARNING, check_response.message)
            faults.append(check_response)

        check_response = self.check_ius_dependency(package_name, package_version)
        if check_response:
            self.logger.log(logging.WARNING, "\tBanned iUS Version Found in %s (%s)" % (package_name, package_version))
            self.logger.log(logging.WARNING, check_response.message)
            faults.append(check_response)

        if "dependencies" in package:
            for dependency in package["dependencies"]:
                self.logger.log(logging.DEBUG, "Checking %s" % dependency)
                check_response = self.check_banned_dependency(dependency,
                                                              version.parse(package["dependencies"][dependency]))
                if check_response:
                    self.logger.log(logging.WARNING,
                                    "\tBanned Version Found in %s (%s)" % (package_name, package_version))
                    self.logger.log(logging.WARNING, check_response.message)
                    faults.append(check_response)

                check_response = self.check_ius_dependency(dependency,
                                                           version.parse(package["dependencies"][dependency]))
                if check_response:
                    self.logger.log(logging.WARNING,
                                    "\tBanned iUS Version Found in %s (%s)" % (package_name, package_version))
                    self.logger.log(logging.WARNING, check_response.message)
                    faults.append(check_response)

        return faults

    def find_banned_versions(self) -> []:
        if "targets" not in self.project_assets:
            raise ValueError("Unable to get targets from project assets")
        targets = self.project_assets["targets"]
        faults = []
        for targetKey in targets:
            self.check_target_version(targetKey)

            for package in targets[targetKey]:
                faults = faults + self.check_package(package, targets[targetKey][package])

        return faults

    def check(self) -> VersionCheckResult:
        self.load_banned_versions()
        self.load_project_assets()
        faults = self.find_banned_versions()

        results = VersionCheckResult()
        results.passed = True
        if len(faults) > 0:
            results.passed = False
            results.faults = faults

        return results


def run(project_asset_file, allowed_ius_state_codes, log_level=logging.INFO):
    checker = VersionChecker(log_level, project_asset_file, allowed_ius_state_codes)
    checker.logger.log(logging.INFO, "Checking for banned versions")
    checker.logger.log(logging.INFO, "Allowing states : %s" % allowed_ius_state_codes)
    results = checker.check()

    if not results.passed:
        checker.logger.log(logging.WARN, "=====\nBanned Packages Found\n=====")
        for fault in results.faults:
            checker.logger.log(logging.WARN, fault.message)
        return 1
    checker.logger.log(logging.INFO, "No Banned Packages Found")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="iUS Version Checker")
    parser.add_argument("--assets", type=str, help="The full path for the project.assets.json to evaluate")
    parser.add_argument("--state_code", type=int, nargs='+', help="The expected state code allowed")
    parser.add_argument("--log_level", type=str, choices=["info", "debug", "warning"], default="info")
    args = parser.parse_args()

    allowed_ius_state_codes = [0]
    for state_code in args.state_code:
        if state_code not in allowed_ius_state_codes:
            allowed_ius_state_codes.append(state_code)

    log_level = logging.INFO
    if args.log_level == "debug":
        log_level = logging.DEBUG
    if args.log_level == "warning":
        log_level = logging.WARNING
    exit_code = run(args.assets, allowed_ius_state_codes, log_level)
    exit(exit_code)
