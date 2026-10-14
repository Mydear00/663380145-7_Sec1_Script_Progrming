import json
import os

class ConfigParser:
    """Load and validate the JSON workflow configuration."""
    def __init__(self, config_path):
        self.config_path = config_path

    def load_config(self):
        if not os.path.isfile(self.config_path):
            raise FileNotFoundError(f"ไม่พบไฟล์ config: {self.config_path}")
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except json.JSONDecodeError as exc:
            raise ValueError(f"รูปแบบ JSON ไม่ถูกต้อง: {exc}") from exc

        for field in ("input_file", "output_file", "tasks"):
            if field not in config:
                raise ValueError(f"ขาดฟิลด์ที่จำเป็น: {field}")
        if not isinstance(config["tasks"], list):
            raise ValueError("'tasks' ต้องเป็น list")
        for i, task in enumerate(config["tasks"], start=1):
            if not isinstance(task, dict) or "type" not in task:
                raise ValueError(f"Task {i} ต้องเป็น object และมีฟิลด์ 'type'")
        return config
