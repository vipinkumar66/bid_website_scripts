import os
import time
import datetime
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium import webdriver

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

cwd = os.path.abspath(os.getcwd())
download_directory = os.path.join(cwd, 'csvfiles', datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S'))

if not os.path.exists(download_directory):
    os.makedirs(download_directory)

# Set Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')  # Run in headless mode
chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration (optional)
chrome_options.add_experimental_option('prefs', {
    'download.default_directory': download_directory,
    'download.prompt_for_download': False,
    'download.directory_upgrade': True,
    'safebrowsing.enabled': True
})

# Create a new instance of the ChromeDriver with the specified options

driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
driver.implicitly_wait(10)


driver.get("https://autoauctions.gsa.gov/GSAAutoAuctions/VehicleListing")
driver.maximize_window()

# SELECT ALL THE VEHICLE TYPE AND SEARCH
driver.find_elements(By.CLASS_NAME, "vehicle_sub")[8].click()
time.sleep(2)

driver.find_element(By.CSS_SELECTOR, "input[name='fromDate']").send_keys("2023-04-27")
driver.find_element(By.CSS_SELECTOR, "input[name='toDate']").send_keys("2023-05-27")

# driver.find_element(By.ID, "checkUncheckVehicleType").click()
time.sleep(5)
driver.find_element(By.XPATH, '//div[@class = "align-right"][2]/input[1]').click()

driver.find_element(By.XPATH, '//input[@class = "excelsx-export-btn"]').click()
time.sleep(4)

window_handles = driver.window_handles

# Switch focus to the most recently opened window
recent_window = window_handles[-1]
driver.switch_to.window(recent_window)

time.sleep(60)




