import json
from pathlib import Path
from .utils import setup_logging

logger = setup_logging(__name__)

class ConfigParser:
    def __init__(self, config_path):
        self.config_path = Path(config_path)
        self.config = {}

    def load_config(self):
        if not self.config_path.is_file():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        try:
            self.config = json.loads(self.config_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON configuration: {exc}") from exc
        self._validate_config()
        logger.info("Configuration loaded and validated: %s", self.config_path)
        return self.config

    def _validate_config(self):
        if not isinstance(self.config, dict) or not isinstance(self.config.get("tasks"), list):
            raise ValueError("Configuration must contain a 'tasks' list.")
        allowed = {"send_email", "send_sms", "process_inbox", "log_message"}
        for index, task in enumerate(self.config["tasks"]):
            if not isinstance(task, dict) or not task.get("name") or not task.get("type"):
                raise ValueError(f"Task #{index + 1} must include name and type.")
            if task["type"] not in allowed:
                raise ValueError(f"Unsupported task type {task['type']!r} in task #{index + 1}.")
            if not isinstance(task.get("parameters", {}), dict):
                raise ValueError(f"Task #{index + 1} parameters must be an object.")
