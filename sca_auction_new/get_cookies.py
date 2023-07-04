import selenium
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor

from trial import ScaAuctionScrapper

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')  # Run in headless mode
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1920,1080')

max_attempts = 3
attempt = 1

while attempt <= max_attempts:
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install(),
                                        options=chrome_options)
        break  # If no exception occurs, break out of the loop
    except selenium.common.exceptions.SessionNotCreatedException:
        attempt += 1
        if attempt <= max_attempts:
            print(f"Attempt {attempt}/{max_attempts} failed. Retrying...")
        else:
            print("Maximum attempts reached. Failed to create WebDriver.")

if driver:
    driver.delete_all_cookies()
    driver.get("https://sca.auction/en/vehicle/search/indexAjax")
    # input_element = driver.find_element(By.ID, "mainSearchLabel")
    # input_element.send_keys("Your desired value")

    # # Simulate pressing the Enter key
    # input_element.send_keys(Keys.ENTER)
    # time.sleep(5)

    selenium_cookies = driver.get_cookies()
    cookies2 = {cookie['name']: cookie['value'] for cookie in selenium_cookies}



def run_scrapper():
    try:
        sca_scrapper = ScaAuctionScrapper()
        sca_scrapper.make_first_request(cookies2)

        with ThreadPoolExecutor() as executor:
            executor.map(sca_scrapper.get_all_vehicle_links, cookies2,
                        range(2, sca_scrapper.max_page+1))

        with ThreadPoolExecutor() as executor:
            executor.map(sca_scrapper.get_vehicle_details, cookies2,
                        sca_scrapper.all_links)

        driver.quit()
    except Exception as e:
        print(e)


run_scrapper()