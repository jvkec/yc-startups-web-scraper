# YC Startups Web Scraper

This script scrapes detailed information about startups listed on Y Combinator’s website. It caps at 1000 of the most popular companies.

NOTE: You can actually get most of the information on the page of companies using the public Algolia API. The 1000 company cap is still in place, however.

## Features

- Collects:
  - Company name
  - Description
  - Website
  - YC batch (e.g., W24)
  - Tags (industry and location)
  - YC company page URL
- Scrolls to load all companies
- Saves everything to a CSV

## Requirements

- Python 3
- Google Chrome installed
- Install Python packages:
  ```bash
  pip install -r requirements.txt
  ```

> ✅ No need to install ChromeDriver manually — Selenium handles it.

## How to Use

Run the script:
```bash
python main_selenioum.py
```
or
```bash
python main_algolia_api.py
```

A file called `yc_companies.csv` will be created with the results.

## Output

CSV columns:
- `name`
- `description`
- `website`
- `batch`
- `yc_url`
- `tags` (separated by `|`)

## License

MIT