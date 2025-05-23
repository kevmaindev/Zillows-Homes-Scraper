# Zillow Scraper with Scrapy

This project scrapes real estate listings from Zillow using Scrapy with `scrapy-impersonate` to avoid detection. It extracts detailed property information for specified cities.

## Requirements

- Python 3.7+
- Scrapy
- scrapy-impersonate

NOTE: Consider using a virtual environment while installing scrapy.

## Installation

```bash
pip install scrapy scrapy-impersonate
```

## Cities file
 - Check the json file named `Most populous cities in the United States.json` for city names and urls references.

## Data Fields Collected

The scraper extracts the following fields for each listing:
- `home_type` (e.g., "SINGLE_FAMILY")
- `posted` (time on market)
- `Broker Name`
- `home_status` (e.g., "FOR_SALE")
- `home_price`
- `home_address` (full address)
- `home_zipcode`
- `num_beds` (number of bedrooms)
- `num_baths` (number of bathrooms)
- `home_area` (square footage)
- `home_URL` (Zillow listing URL)
- `home_main_image` (primary photo URL)

## Running the Scraper

Execute the spider with:

```bash
scrapy crawl spider
```

## Output Format

Results are saved with the structure shown above, in both JSON and CSV format in a folder named `Homes Data` in a folder of the date the script is run.

## Notes

- Uses `scrapy-impersonate` to mimic browser behavior
- Respects Zillow's robots.txt and rate limits
- Consider adding delays between requests (configure in spider settings)
- For production use, consider rotating user agents and proxies