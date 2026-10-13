
# Agentic Web Scraper

A configuration-driven web scraper built with Python and Selenium.

This educational project demonstrates browser automation, pagination, structured data extraction, error handling, logging, and JSON persistence.

## Features

- Loads scraping instructions from a JSON configuration file.
- Uses Selenium to automate Google Chrome.
- Extracts product names, prices, product URLs, and image URLs.
- Supports pagination with a configurable page limit.
- Uses explicit waits to handle page loading.
- Handles temporary browser errors.
- Removes duplicate products.
- Saves scraped results to `data/scraped_products.json`.
- Includes ethical web scraping guidelines.

## Project Structure

```text
agentic-web-scraper/
├── src/
│   ├── __init__.py
│   ├── scraper_agent.py
│   ├── config_parser.py
│   ├── data_models.py
│   ├── utils.py
│   └── driver_manager.py
├── configs/
│   └── example_site_config.json
├── data/
│   └── scraped_products.json
├── docs/
│   └── ETHICS.md
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Requirements

- Python 3.10 or newer
- Google Chrome
- Internet access for the example website and driver setup

## Setup on Windows PowerShell

Open PowerShell in the project root directory.

### 1. Create a virtual environment

```powershell
python -m venv .venv
```

### 2. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Run the scraper

```powershell
python main.py
```

## Configuration

Configuration file: `configs/example_site_config.json`

Important settings:

- `start_url`: Website URL to scrape.
- `max_pages`: Maximum number of pages to process.
- `delay_between_pages`: Delay between pages in seconds.
- `item_container_selector`: CSS selector for product containers.
- `pagination_selector`: CSS selector for the next-page link.
- `item_data_selectors`: CSS selectors for product fields.

## Output

Scraped products are saved to:

`data/scraped_products.json`

Each product contains:

- `name`
- `price`
- `description`
- `url`
- `image_url`

## Troubleshooting

### Missing Python packages

```powershell
python -m pip install -r requirements.txt
```

### Invalid JSON configuration

```powershell
python -m json.tool configs\example_site_config.json
```

### Check Python syntax

```powershell
python -m compileall src main.py
```

### ChromeDriver startup errors

Check that Google Chrome is installed and that internet access is available if the browser driver needs to be downloaded.

### No products found

Verify the website URL and CSS selectors in `configs/example_site_config.json`.

## Ethical Considerations

- Respect website terms of service and `robots.txt`.
- Use reasonable delays between pages.
- Do not bypass authentication, CAPTCHAs, paywalls, or access controls.
- Avoid collecting personal or sensitive information.
- Respect copyright and website data policies.

See `docs/ETHICS.md` for additional guidelines.

## Educational Purpose

This project is intended for learning Python, Selenium, browser automation, web scraping, and structured data extraction.
