# YC Startups Web Scraper

This script scrapes detailed information about startups listed on Y Combinator’s website.

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
python main.py
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