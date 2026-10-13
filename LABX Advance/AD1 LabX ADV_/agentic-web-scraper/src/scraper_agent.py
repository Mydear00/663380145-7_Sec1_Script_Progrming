import logging
import time
from urllib.parse import urljoin

from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .data_models import Product
from .driver_manager import DriverManager
from .utils import save_data_to_json


logger = logging.getLogger(__name__)


class ScraperAgent:
    """Configuration-driven agent for scraping product listing pages."""

    def __init__(self, config, browser="chrome", headless=True):
        self.config = config
        self.driver_manager = DriverManager(
            browser_name=browser,
            headless=headless,
        )
        self.driver = None
        self.scraped_products = []
        self.max_pages = config.get("max_pages", 5)
        self.seen_products = set()

        logger.info("Scraper agent initialized for %s", config["start_url"])

    def _get_text(self, parent, selector):
        """Extract text safely from a child element."""
        if not selector:
            return None

        try:
            return parent.find_element(By.CSS_SELECTOR, selector).text.strip()
        except (NoSuchElementException, StaleElementReferenceException):
            return None

    def _get_attribute(self, parent, selector, attribute):
        """Extract an attribute safely and resolve relative URLs."""
        if not selector:
            return None

        try:
            value = parent.find_element(
                By.CSS_SELECTOR, selector
            ).get_attribute(attribute)

            if not value:
                return None

            value = value.strip()
            if attribute in ("href", "src"):
                return urljoin(self.driver.current_url, value)
            return value
        except (NoSuchElementException, StaleElementReferenceException):
            return None

    def _parse_product(self, element):
        """Build a Product from the configured selectors."""
        selectors = self.config["item_data_selectors"]

        name = self._get_text(element, selectors.get("name"))
        price = self._get_text(element, selectors.get("price"))

        if not name or not price:
            logger.debug("Skipped an item because name or price was missing.")
            return None

        return Product(
            name=name,
            price=price,
            description=self._get_text(element, selectors.get("description")),
            url=self._get_attribute(element, selectors.get("url"), "href"),
            image_url=self._get_attribute(
                element, selectors.get("image_url"), "src"
            ),
        )

    def scrape_page(self):
        """Extract products from the current page."""
        logger.info("Scraping page: %s", self.driver.current_url)

        try:
            elements = WebDriverWait(self.driver, 15).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, self.config["item_container_selector"])
                )
            )
        except TimeoutException:
            logger.warning("No product containers appeared on this page.")
            return

        logger.info("Found %s product containers.", len(elements))

        for element in elements:
            try:
                product = self._parse_product(element)
                if product is None:
                    continue

                unique_key = product.url or f"{product.name}|{product.price}"
                if unique_key in self.seen_products:
                    continue

                self.seen_products.add(unique_key)
                self.scraped_products.append(product.to_dict())
            except StaleElementReferenceException:
                logger.warning("An item changed while being read; skipped.")
            except Exception:
                logger.exception("Could not parse one product.")

    def run(self):
        """Run the configured scraping and pagination loop."""
        self.driver = self.driver_manager.get_driver()

        if self.driver is None:
            logger.error("Scraping stopped because WebDriver could not start.")
            return

        try:
            self.driver.get(self.config["start_url"])

            for page_number in range(1, self.max_pages + 1):
                logger.info("Processing page %s/%s", page_number, self.max_pages)
                self.scrape_page()

                if page_number >= self.max_pages:
                    logger.info("Reached the configured page limit.")
                    break

                selector = self.config.get("pagination_selector")
                if not selector:
                    logger.info("No pagination selector configured.")
                    break

                old_url = self.driver.current_url

                try:
                    next_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                except TimeoutException:
                    logger.info("No next-page link found. Pagination finished.")
                    break

                if not next_button.is_displayed() or not next_button.is_enabled():
                    logger.info("Next-page link is not available.")
                    break

                try:
                    next_button.click()
                    WebDriverWait(self.driver, 10).until(
                        EC.url_changes(old_url)
                    )
                except TimeoutException:
                    logger.warning("Page URL did not change after clicking Next.")
                    break
                except (StaleElementReferenceException, WebDriverException):
                    logger.exception("Could not navigate to the next page.")
                    break

                time.sleep(self.config.get("delay_between_pages", 2))

        except Exception:
            logger.exception("Unexpected error during scraping.")
        finally:
            self.driver_manager.quit_driver()
            logger.info(
                "Scraping finished. Total unique products: %s",
                len(self.scraped_products),
            )

            save_data_to_json(
                self.scraped_products,
                "scraped_products.json",
                directory="data",
            )