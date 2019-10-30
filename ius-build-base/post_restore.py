import sys
from pathlib import Path
import versionchecker

def get_project_assets_files(base_path):
    files = []
    for asset_file in Path(base_path).rglob("project.assets.json"):
        full_path = Path(asset_file).resolve()
        files.append(str(full_path))
    return files


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("The first argument must be the base folder to check")
    files = get_project_assets_files(sys.argv[1])
    for file in files: 
        versionchecker.run(file)
