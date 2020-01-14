import sys
from pathlib import Path
import versionchecker
import argparse
import logging

def get_project_assets_files(base_path):
    files = []
    for asset_file in Path(base_path).rglob("project.assets.json"):
        full_path = Path(asset_file).resolve()
        files.append(str(full_path))
    return files


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="iUS Version Checker")
    parser.add_argument("--base_path", type=str, help="The base path to search for project.assets.json files")
    parser.add_argument("--state_code", type=int, nargs='+', help="The expected state code allowed")
    parser.add_argument("--log_level", type=str, choices=["info", "debug", "warning"], default="info")
    args = parser.parse_args()

    # Always allow state code 0
    allowed_ius_state_codes = [0]
    for state_code in args.state_code:
        if state_code not in allowed_ius_state_codes:
            allowed_ius_state_codes.append(state_code)

    log_level = logging.INFO
    if args.log_level == "debug":
        log_level = logging.DEBUG
    if args.log_level == "warning":
        log_level = logging.WARNING

    files = get_project_assets_files(args.base_path)
    exit_code = 0
    for file in files: 
        check_result = versionchecker.run(file, allowed_ius_state_codes, log_level)
        # find the max exit code
        if check_result > exit_code:
            exit_code = check_result
    exit(exit_code)
