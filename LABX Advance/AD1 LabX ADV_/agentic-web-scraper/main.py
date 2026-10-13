import logging
from pathlib import Path

from src.config_parser import ConfigParser
from src.scraper_agent import ScraperAgent


BASE_DIR = Path(__file__).resolve().parent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def main():
    """Load configuration and start the scraper agent."""
    config_path = BASE_DIR / "configs" / "example_site_config.json"

    try:
        config = ConfigParser(str(config_path)).load_config()
        agent = ScraperAgent(config, browser="chrome", headless=True)
        agent.run()
    except (FileNotFoundError, ValueError):
        logging.exception("Could not load the scraper configuration.")
    except Exception:
        logging.exception("The application encountered an unexpected error.")


if __name__ == "__main__":
    main()