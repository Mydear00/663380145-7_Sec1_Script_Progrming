import json
import logging
import time
from pathlib import Path

from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


logger = logging.getLogger(__name__)


def wait_for_element(driver, by, value, timeout=10):
    """Wait until an element is visible; return None on timeout."""
    if not value:
        return None

    try:
        return WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((by, value))
        )
    except TimeoutException:
        logger.warning("Timed out waiting for element: %s", value)
        return None


def robust_click(driver, by, value, max_attempts=3, delay_between_attempts=1):
    """Retry clicking an element when a temporary browser error occurs."""
    for attempt in range(1, max_attempts + 1):
        try:
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((by, value))
            )
            element.click()
            return True
        except (TimeoutException, StaleElementReferenceException, WebDriverException):
            logger.warning(
                "Click attempt %s/%s failed for selector %s",
                attempt,
                max_attempts,
                value,
            )
            if attempt < max_attempts:
                time.sleep(delay_between_attempts)

    logger.error("Could not click element: %s", value)
    return False


def save_data_to_json(data, filename, directory="data"):
    """Save scraped dictionaries as UTF-8 JSON."""
    output_dir = Path(directory)
    output_dir.mkdir(parents=True, exist_ok=True)
    filepath = output_dir / filename

    try:
        with filepath.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        logger.info("Saved %s records to %s", len(data), filepath)
        return True
    except (OSError, TypeError, ValueError):
        logger.exception("Could not save JSON file: %s", filepath)
        return False


def scroll_to_bottom(driver):
    """Scroll to the bottom of a page that loads content while scrolling."""
    driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);"
    )
    time.sleep(1)