import datetime
import json
import logging
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def setup_logging(name, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger

def get_env_variable(name, default=None, required=False):
    value = os.getenv(name, default)
    if required and not value:
        raise ValueError(f"Environment variable '{name}' is missing. Check your .env file.")
    return value

def ensure_directory_exists(path):
    Path(path).mkdir(parents=True, exist_ok=True)

def log_audit_entry(audit_log_list, status, message, task_type="N/A", details=None):
    audit_log_list.append({
        "timestamp": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        "status": status, "task_type": task_type, "message": message, "details": details or {}
    })

def write_json(path, data):
    ensure_directory_exists(Path(path).parent)
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
