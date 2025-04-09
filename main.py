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

    # Parse w/ BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    companies = []

    # Find all company elements
    company_elements = soup.select('a[href^="/companies/"]')

    for element in company_elements:
        company_url = 'https://www.ycombinator.com' + element['href']
        name_elem = element.find("span", class_=lambda x: x and "_coName_" in x)
        company_name = name_elem.get_text(strip=True) if name_elem else "Unknown"
        if company_name:
            companies.append({
                'name': company_name,
                'url': company_url
            })

    logging.info(f"Found {len(companies)} companies.")
    return companies

def main():
    driver = None
    try:
        driver = setup_driver()

        companies = get_company_list(driver)
        companies = companies[:10]

        for c in companies:
            logging.info(c)

    except Exception:
        logging.error("An error occurred:", exc_info=True)
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()