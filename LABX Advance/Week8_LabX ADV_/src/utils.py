import json
from datetime import datetime
from pathlib import Path


def ensure_directory_exists(file_path):
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)


def load_json_file(file_path):
    with open(file_path, "r", encoding="utf-8-sig") as file:
        return json.load(file)


def save_json_file(data, file_path, indent=4):
    ensure_directory_exists(file_path)
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=indent, ensure_ascii=False)


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def resolve_project_path(project_dir, path):
    path = Path(path)
    return path if path.is_absolute() else Path(project_dir) / path
