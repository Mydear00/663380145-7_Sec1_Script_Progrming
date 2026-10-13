import json
from pathlib import Path


class ConfigParser:
    """Load and validate the JSON pipeline configuration."""

    def __init__(self, config_file):
        self.config_file = Path(config_file)

    def load_config(self):
        """Load configuration from a JSON file."""
        try:
            with self.config_file.open(
                "r",
                encoding="utf-8-sig"
            ) as file:
                config = json.load(file)

            return config

        except FileNotFoundError:
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_file}"
            )

        except json.JSONDecodeError as error:
            raise ValueError(
                f"Invalid JSON configuration: {error}"
            ) from error