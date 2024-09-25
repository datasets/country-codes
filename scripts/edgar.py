#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Set up Selenium in headless mode
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize the WebDriver
driver = webdriver.Chrome(options=chrome_options)

def run():
    driver.get(config.EDGAR_URL)
    # Find the first table element on the page
    table = driver.find_element(By.TAG_NAME, 'table')

    # Get all the rows within the table
    rows = table.find_elements(By.TAG_NAME, 'tr')

    # Prepare a list to store the extracted data
    data = []

    # Loop through each row (starting from the second row to skip the header)
    for row in rows[1:]:
        cells = row.find_elements(By.TAG_NAME, 'td')
        
        if len(cells) > 1:  # Make sure there are enough cells
            edgar_code = cells[0].text.strip()  # First column: EDGAR code
            name = cells[1].text.strip()        # Second column: Name
            data.append([edgar_code, name])

    driver.quit()

    # Save the extracted data to a CSV file
    with open(config.EDGAR_FILE_NAME, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        # Write the header
        csv_writer.writerow(config.EDGAR_HEADERS)
        
        # Write the rows
        csv_writer.writerows(data)

if __name__ == '__main__':
    run()