import logging

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


logger = logging.getLogger(__name__)


class DriverManager:
    """Creates and closes a Selenium Chrome WebDriver."""

    def __init__(self, browser_name: str = "chrome", headless: bool = True):
        self.browser_name = browser_name.lower()
        self.headless = headless
        self.driver = None

    def get_driver(self):
        """Initialize Chrome and return the WebDriver."""
        if self.driver is not None:
            return self.driver

        if self.browser_name != "chrome":
            raise ValueError("This project currently supports Chrome only.")

        options = webdriver.ChromeOptions()

        if self.headless:
            options.add_argument("--headless=new")

        options.add_argument("--window-size=1440,1000")
        options.add_argument("--disable-notifications")
        options.add_argument("--log-level=3")

        try:
            service = ChromeService(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.implicitly_wait(2)
            self.driver.set_page_load_timeout(30)
            logger.info("Chrome WebDriver started successfully.")
            return self.driver
        except Exception:
            logger.exception(
                "Could not start Chrome. Check that Google Chrome is installed "
                "and that the computer can download the matching driver."
            )
            self.quit_driver()
            return None

    def quit_driver(self) -> None:
        """Close the browser if it is running."""
        if self.driver is not None:
            try:
                self.driver.quit()
                logger.info("Chrome WebDriver closed.")
            except Exception:
                logger.exception("An error occurred while closing Chrome.")
            finally:
                self.driver = None