#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)

def run():
    driver.get(config.EDGAR_URL)
    table = driver.find_element(By.TAG_NAME, 'table')
    rows = table.find_elements(By.TAG_NAME, 'tr')

    data = []
    start_recording = False  # To start recording rows when "B2, AFGHANISTAN" is found

    for row in rows[1:]:
        cells = row.find_elements(By.TAG_NAME, 'td')
        
        if len(cells) > 1:
            edgar_code = cells[0].text.strip()
            name = cells[1].text.strip()

            # Check if we are at the row where "B2, AFGHANISTAN" appears
            if edgar_code == "B2" and name == "AFGHANISTAN":
                start_recording = True

            # Start appending rows only after "B2, AFGHANISTAN"
            if start_recording:
                data.append([edgar_code, name])

    driver.quit()

    # Save the filtered data to a CSV file
    with open(config.EDGAR_FILE_NAME, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(config.EDGAR_HEADERS)

        csv_writer.writerows(data)

if __name__ == '__main__':
    run()