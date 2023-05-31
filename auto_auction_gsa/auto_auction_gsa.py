import os
import time
from datetime import datetime, timedelta
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium import webdriver

class AutoGSA:
    """
    To download the bid report from GSA fleet website
    """
    def __init__(self):
        """
        Here in the intial step we are creating the
        output folder
        """
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)

        cwd = os.path.abspath(os.getcwd())
        self.download_directory = os.path.join(cwd, 'csvfiles', datetime.now().strftime('%Y-%m-%d_%H_%M_%S'))

        if not os.path.exists(self.download_directory):
            os.makedirs(self.download_directory)

        today = datetime.now().date()
        self.formatted_end_date = today.strftime("%Y-%m-%d")
        start_date = today - timedelta(days=30)
        self.formatted_start_date = start_date.strftime("%Y-%m-%d")

    def set_chrome_options(self):
        """
        Here we will set the chrome options:
        For headless and For downloading directory
        """
        # Set Chrome options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')  # Run in headless mode
        chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_experimental_option('prefs', {
            'download.default_directory': self.download_directory,
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
            'safebrowsing.enabled': True
        })

        # Create a new instance of the ChromeDriver with the specified options

        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        self.driver.implicitly_wait(10)

    def dowload_data_csv(self):
        """
        This will download the csv to the system
        """
        self.driver.get("https://autoauctions.gsa.gov/GSAAutoAuctions/VehicleListing")
        self.driver.maximize_window()

        # SELECT ALL THE VEHICLE TYPE AND SEARCH
        time.sleep(2)
        self.driver.find_elements(By.CLASS_NAME, "vehicle_sub")[8].click()
        time.sleep(2)

        self.driver.find_element(By.CSS_SELECTOR, "input[name='fromDate']").send_keys(self.formatted_start_date)
        self.driver.find_element(By.CSS_SELECTOR, "input[name='toDate']").send_keys(self.formatted_end_date)

        # self.driver.find_element(By.ID, "checkUncheckVehicleType").click()
        time.sleep(5)
        self.driver.find_element(By.XPATH, '//div[@class = "align-right"][2]/input[1]').click()

        self.driver.find_element(By.XPATH, '//input[@class = "excelsx-export-btn"]').click()
        time.sleep(4)

        window_handles = self.driver.window_handles

        # Switch focus to the most recently opened window
        recent_window = window_handles[-1]
        self.driver.switch_to.window(recent_window)
        time.sleep(60)

if __name__ == "__main__":
    start_time = time.time()
    obj = AutoGSA()
    obj.set_chrome_options()
    obj.dowload_data_csv()
    print(f"Downloading of csv took : {time.time() - start_time} seconds")




