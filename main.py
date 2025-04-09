import requests
from bs4 import BeautifulSoup
import time
import random
import csv
import logging
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def get_company_list(driver, start_url='https://www.ycombinator.com/companies'):
    driver.get(start_url) # Open URL

    # Wait for page to load and company elements to appear
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href^="/companies/"]')))
    

    last_height = driver.execute_script("return document.body.scrollHeight")
    
    # -- TESTING --
    scroll_count = 0
    max_scrolls = 10

    while scroll_count < max_scrolls:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        scroll_count += 1

    # -- ACTUAL IMPLEMENTATION --
    # while True:
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #     time.sleep(2)
    #     new_height = driver.execute_script("return document.body.scrollHeight")
    #     if new_height == last_height: # Reached end of scroll
    #         break
    #     last_height = new_height
    
    # Parse w/ BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    companies = []

    # Find all company elements
    company_elements = soup.select('a[href^="/companies/"]')

    for element in company_elements:
        href = element['href']
        if href.strip() == "/companies/founders":
            continue
        company_url = 'https://www.ycombinator.com' + href
        name_elem = element.find("span", class_=lambda x: x and "_coName_" in x)
        company_name = name_elem.get_text(strip=True) if name_elem else "Unknown"
        if company_name:
            companies.append({
                'name': company_name,
                'url': company_url
            })

    logging.info(f"Found {len(companies)} companies.")
    return companies

def get_company_details(driver, company_url):
    logging.info(f"Fetching details for {company_url}")
    try:
        time.sleep(random.uniform(1, 2))
        
        driver.get(company_url)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # .get_text(strip=True) grabs contents in side the <div class=...> ... <div>

        # Company description
        desc_elem = soup.find("div", class_="prose max-w-full whitespace-pre-line")
        description = desc_elem.get_text(strip=True) if desc_elem else ""

        # Batch
        batch_elem = soup.find("span", string=lambda s: s and s.startswith(("W", "S")) and len(s) == 3)
        batch = batch_elem.get_text(strip=True) if batch_elem else ""

        # Company website
        website = ""
        for a in soup.find_all("a", href=True, target="_blank"):
            visible_text = a.get_text(strip=True)
            href = a["href"]
            if href.startswith("http") and visible_text and visible_text in href:
                website = href
                break

        # Tags
        tag_elements = soup.select('a[href^="/companies/industry/"], a[href^="/companies/location/"]')
        tags = [tag.get_text(strip=True) for tag in tag_elements]
        tags_string = " | ".join(tags)

        return {
            'description': description,
            'batch': batch,
            'website': website,
            'tags': tags_string
        }
    except Exception as e:
        logging.error(f"Error fetching company details for {company_url}: {e}")
        return {
            'description': "",
            'batch': "",
            'website': "",
            'tags': ""
        }

def save_to_csv(companies, filename='yc_companies.csv'):
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'description', 'website', 'batch', 'yc_url', 'tags']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for company in companies:
                writer.writerow({
                    'name': company['name'],
                    'description': company.get('description', ''),
                    'website': company.get('website', ''),
                    'batch': company.get('batch', ''),
                    'yc_url': company['url'],
                    'tags': company.get('tags', '')
                })
        
        logging.info(f"Successfully saved {len(companies)} companies to {filename}")
    
    except Exception as e:
        logging.error(f"Error saving to CSV: {e}")

def main():
    driver = None
    try:
        driver = setup_driver()

        companies = get_company_list(driver)
        companies = companies[:10]

        for c in companies:
            logging.info(c)

        for i, company in enumerate(companies):
            logging.info(f"Processing company {i+1}/{len(companies)}: {company['name']}")
            details = get_company_details(driver, company['url'])
            companies[i].update(details)
        
        save_to_csv(companies)
        
        logging.info("Scraping completed successfully")

    except Exception:
        logging.error("An error occurred:", exc_info=True)
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()