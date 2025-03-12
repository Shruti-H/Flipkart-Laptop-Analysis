from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import logging
import os
import pandas as pd
import traceback
from datetime import datetime
from bs4 import BeautifulSoup

def setup_logging():
    try:
        # Create 'Logs/' directory if it doesn't exist
        os.makedirs(LOGS_DIR, exist_ok=True)
        
        # Generate timestamped log file name inside 'Logs/' directory
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_filename = os.path.join(LOGS_DIR, f'flipkart_scraper_{timestamp}.log')

        # Configure logging (ONLY log to file, NOT console)
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler(log_filename, mode="a")]  # Only file logging
        )
        return logging.getLogger()
    except Exception as e:
        print(f"Error setting up logging: {e}")
        exit(1)

def setup_webdriver():
    # Set up WebDriver path
    webdriver_path = r"C:\Users\hp\Downloads\chromedriver-win64\chromedriver.exe"

    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--incognito")  # Incognito mode
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")  # Fake user-agent

    # Initialize WebDriver with options
    service_object = Service(executable_path=webdriver_path)
    driver = webdriver.Chrome(service=service_object, options=chrome_options)
    
    # Set page load timeout to handle slow pages
    driver.set_page_load_timeout(180)
    
    # Implicit wait for elements to be ready
    driver.implicitly_wait(2)
    
    return driver

def scrape_product_links(driver, url):
    try:
        logger.info(f"Fetching URL: {url}")
        driver.get(url)

        # Explicit wait: Wait up to 10 seconds for at least one product link to be present
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, "//a[@class='CGtC98']")))

        product_links = driver.find_elements(By.XPATH, "//a[@class='CGtC98']")
        return product_links
    except Exception as e:
        logger.error(f"Error fetching page {url}: {e}")
        return []

def extract_laptop_specs(soup):
    laptop_specs = {field: 'N/A' for field in FIELDS_TO_EXTRACT}
    laptop_specs['Laptop Name'] = soup.find('span', class_='VU-ZEz').text.strip() if soup.find('span', class_='VU-ZEz') else 'N/A'
    laptop_specs['Rating'] = soup.find('div', class_='XQDdHH').text.strip() if soup.find('div', class_='XQDdHH') else 'N/A'
    laptop_specs['Rating/Review Count'] = soup.find('span', class_='Wphh3N').text.strip() if soup.find('span', class_='Wphh3N') else 'N/A'
    laptop_specs['Final price'] = soup.find('div', class_='Nx9bqj').text.strip()[1:] if soup.find('div', class_='Nx9bqj') else 'N/A'
    laptop_specs['MRP'] = soup.find('div', class_='yRaY8j').text.strip()[1:] if soup.find('div', class_='yRaY8j') else 'N/A'
    laptop_specs['Discount'] = soup.find('div', class_='UkUFwK').text.strip() if soup.find('div', class_='UkUFwK') else 'N/A'

    rows = soup.find_all('tr', class_='WJdYP6 row')
    for row in rows:
        category_tag = row.find('td', class_='+fFi1w')
        if category_tag:
            category = category_tag.text.strip()
            if category in FIELDS_TO_EXTRACT:
                value_tag = category_tag.find_next_sibling('td', class_='Izz52n')
                value = value_tag.text.strip() if value_tag else 'N/A'
                laptop_specs[category] = value
        else:
            logger.warning("Category tag missing!")

    return laptop_specs

def scrape_product_details(driver):
    page_count = 1
    all_laptops = []
    try:
        while page_count <= 41:
            retry_count = 0  # Initialize retry count
            while retry_count < MAX_RETRIES:
                try:
                    url = f"https://www.flipkart.com/search?query={QUERY}&page={page_count}"
                    product_link_tags = scrape_product_links(driver, url)

                    if not product_link_tags:
                        logger.warning(f"No product links found on Page {page_count}. Retrying ({retry_count + 1}/{MAX_RETRIES})...")
                        retry_count += 1
                        time.sleep(3)  # Short wait before retrying
                        continue  # Retry this page
                    logger.info(f"Found {len(product_link_tags)} product links on Page {page_count}")

                    for product_link_tag in product_link_tags:
                        product_link = product_link_tag.get_attribute("href")
                        logger.info(f"Scraping laptop details from product link: {product_link}")
                        driver.execute_script(f"window.open('{product_link}');")
                        time.sleep(2)
                        driver.switch_to.window(driver.window_handles[-1])
                        time.sleep(random.uniform(1, 2))  # Random delay

                        # Parse the product page
                        soup = BeautifulSoup(driver.page_source, 'html.parser')
                        laptop_specs = extract_laptop_specs(soup)
                        laptop_specs['Product URL'] = product_link

                        all_laptops.append(laptop_specs)
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        logger.info(f"Scraped laptop details.")

                    break  # Exit retry loop if successful
                except Exception as e:
                    retry_count += 1
                    logger.error(f"Error on Page {page_count}: {e}")
                    logger.error(traceback.format_exc())
                    if retry_count >= MAX_RETRIES:
                        logger.error(f"Skipping Page {page_count} after {MAX_RETRIES} failed attempts.")
            page_count += 1  # Move to next page
    finally:
        save_to_csv(all_laptops, "flipkart_laptops_full.csv")
        driver.quit()
        logger.info("Scraping Complete.")

def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    output_csv = os.path.join(BASE_DIR, "Data", filename)
    df.to_csv(output_csv, index=False, encoding="utf-8")
    logger.info(f"Data saved to {output_csv}")


if __name__ == '__main__':
    # Directory to save data
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LOGS_DIR = os.path.join(BASE_DIR, "Logs")
    DATA_DIR = os.path.join(BASE_DIR, "Data")
    os.makedirs(DATA_DIR, exist_ok=True)

    MAX_RETRIES = 3  # Maximum number of retries per page
    QUERY = 'laptops'
    BASE_URL = "https://www.flipkart.com"

    FIELDS_TO_EXTRACT = (
        "Model Name", "Type", "Processor Brand", "Processor Name", "Processor Generation",
        "RAM", "RAM Type", "Storage Type", "Storage Capacity", "Graphic Processor",
        "Screen Size", "Screen Resolution", "Screen Type", "Weight", "Dimensions",
        "USB Port", "HDMI Port", "Wireless LAN", "Bluetooth", "Battery Cell",
        "Battery Backup", "Web Camera", "Backlit Keyboard", "Warranty Summary"
    )

    logger = setup_logging()
    driver = setup_webdriver()
    scrape_product_details(driver)