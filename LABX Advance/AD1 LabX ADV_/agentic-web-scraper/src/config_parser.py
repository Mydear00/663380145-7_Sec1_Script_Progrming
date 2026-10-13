import json
from pathlib import Path
from typing import Any


class ConfigParser:
    """Loads and validates a JSON scraping configuration."""

    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        self.config: dict[str, Any] = {}

    def load_config(self) -> dict[str, Any]:
        """Load the JSON configuration and validate its contents."""
        if not self.config_path.is_file():
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_path}"
            )

        try:
            with self.config_path.open("r", encoding="utf-8-sig") as file:
                self.config = json.load(file)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON configuration: {exc}") from exc

        self._validate_config()
        print(f"Configuration loaded: {self.config_path}")
        return self.config

    def _validate_config(self) -> None:
        if not isinstance(self.config, dict):
            raise ValueError("The configuration root must be a JSON object.")

        required = (
            "start_url",
            "pagination_selector",
            "item_container_selector",
            "item_data_selectors",
        )

        for field in required:
            if field not in self.config:
                raise ValueError(f"Missing required config field: {field}")

        if not isinstance(self.config["start_url"], str):
            raise ValueError("'start_url' must be a string.")

        if not self.config["start_url"].startswith(("http://", "https://")):
            raise ValueError("'start_url' must start with http:// or https://.")

        for field in ("pagination_selector", "item_container_selector"):
            if not isinstance(self.config[field], str):
                raise ValueError(f"'{field}' must be a CSS selector string.")

        selectors = self.config["item_data_selectors"]
        if not isinstance(selectors, dict):
            raise ValueError("'item_data_selectors' must be a JSON object.")

        for field in ("name", "price"):
            if not isinstance(selectors.get(field), str) or not selectors[field].strip():
                raise ValueError(
                    f"'item_data_selectors.{field}' must be a non-empty string."
                )

        for field, selector in selectors.items():
            if selector is not None and not isinstance(selector, str):
                raise ValueError(
                    f"Selector '{field}' must be a string or null."
                )

        max_pages = self.config.get("max_pages", 5)
        if not isinstance(max_pages, int) or isinstance(max_pages, bool) or max_pages < 1:
            raise ValueError("'max_pages' must be a positive integer.")

        delay = self.config.get("delay_between_pages", 2)
        if not isinstance(delay, (int, float)) or isinstance(delay, bool) or delay < 0:
            raise ValueError("'delay_between_pages' must be a non-negative number.")

        self.config["max_pages"] = max_pages
        self.config["delay_between_pages"] = delay