"""
Importing important libraries
"""
import os
import re
import time
import csv
from datetime import datetime
import selenium
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from constants import headers, folder_name

class CarsAndBids:
    """Scrap details about Auctions"""
    def __init__(self):
        """
        Initalizer function
        """
        self.driver = None
        self.warning = 0
        self.url = f"https://carsandbids.com/"
        self.car_urls = []

    def create_empty_csv(self):
        """
        Create the output folder and empty csv into it
        """
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        with open(f"{folder_name}/carsandbids.csv", mode='w',
                  newline='', encoding='utf-8') as csv_file:
            self.writer = csv.writer(csv_file)
            self.writer.writerow(headers)

    def create_driver(self):
        """
        Setup chrome driver to scrap the data
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')  # Run in headless mode
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1920,1080')

        max_attempts = 3
        attempt = 1

        while attempt <= max_attempts:
            try:
                self.driver = webdriver.Chrome(ChromeDriverManager().install(),
                                               options=chrome_options)
                break  # If no exception occurs, break out of the loop
            except selenium.common.exceptions.SessionNotCreatedException:
                attempt += 1
                if attempt <= max_attempts:
                    print(f"Attempt {attempt}/{max_attempts} failed. Retrying...")
                else:
                    print("Maximum attempts reached. Failed to create WebDriver.")

        if self.driver:
            self.driver.get(self.url)
            time.sleep(5)
        else:
            print("Failed to create WebDriver after multiple attempts.")

    def get_vehicle_url(self):
        """
        To get the url for each item
        """
        page_source = self.driver.page_source

        soup = bs(page_source, "lxml")

        unorganized_list = soup.find_all("ul", class_="auctions-list")

        if unorganized_list:
            list_items = unorganized_list[0].find_all('li')

            for li in list_items:
                anchor_tag = li.find('a')
                if anchor_tag:
                    href = anchor_tag['href']
                    self.car_urls.append(f"https://carsandbids.com{href}")
                else:
                    pass
        else:
            print("No unorganized list with class 'auctions-list' found.")

    def get_vehicle_data(self):
        """
        To get  all the data related to bid vehicle
        """
        for url in self.car_urls:
            print(f"Scraping info from: {url}")

            if self.warning == 20:
                self.driver.delete_all_cookies()
                self.warning = 0
                time.sleep(20)
            else:
                self.driver.get(url)

                time.sleep(5)

                page_source = self.driver.page_source
                soup = bs(page_source, "lxml")
                title = soup.find("div", class_="auction-title").find("h1")
                if title:
                    item = title.text
                else:
                    item = ""
                details_table = soup.find("div", class_="quick-facts")

                # vehicle details
                (make, model, vin, body_style, color, drive,
                engine, transmission)  = self.vehicle_details(details_table)

                #Location details
                (location_zip4, location_city, location_state,
                location_country, location_zip5) = self.location_details(details_table)

                # Image details
                image_thumbnail, images = self.image_details(soup)

                currency_code = "$"


                # Find buy it now price
                bid_attribute = soup.find_all("span", class_="bid-value")[0]
                buy_it_now_price = bid_attribute.text if bid_attribute else ""

                timestamp = datetime.now()

                yard_number = yard_name = sale_date = day_of_week = sale_time =\
                lot = vehicle_type = production_year = model_details = damage_description =\
                secondary_damage = sale_title_state = sale_title_type = has_keys =\
                lot_cond_code = odometer =odometer_brand = est_retail_value = repair_cost =\
                fuel_type = cylinders = runs_drives = sale_status = high_bid_non_vix_sealed_vix =\
                special_note = create_date_time = grid_row = current_bid = trim = last_updated_time =\
                rentals = copart_select = source = time_zone = ""


                data = [yard_number, yard_name, sale_date, day_of_week, sale_time, time_zone, item, lot,
                    vehicle_type, production_year, make, model, model_details, body_style, color, damage_description,
                    secondary_damage, sale_title_state, sale_title_type, has_keys, lot_cond_code, vin, odometer,
                    odometer_brand, est_retail_value, repair_cost, engine, drive, transmission,
                    fuel_type, cylinders, runs_drives, sale_status, high_bid_non_vix_sealed_vix, special_note,
                    location_city, location_state, location_zip5, location_zip4, location_country, currency_code,
                    image_thumbnail, create_date_time, grid_row, current_bid, buy_it_now_price, images, trim,
                    last_updated_time, rentals, copart_select, source, timestamp]

                with open(f"{folder_name}/carsandbids.csv", "a", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow(data)

                self.warning +=1
        print("ALL URLS ARE SCRAPPED")
        self.driver.quit()

    def vehicle_details(self, table_data):
        """
        This will get all the vehicle details
        """

        make_attribute = table_data.find("dt", string="Make")
        make = make_attribute.find_next("dd").text if make_attribute else ""

        # Find model
        model_attribute = table_data.find("dt", string="Model")
        model = model_attribute.find_next("dd").text if model_attribute else ""

        # Find VIN
        vin_attribute = table_data.find("dt", string="VIN")
        vin = vin_attribute.find_next("dd").text if vin_attribute else ""

        # Find body style
        body_style_attribute = table_data.find("dt", string="Body Style")
        body_style = body_style_attribute.find_next("dd").text if body_style_attribute else ""

        # Find exterior color
        color_attribute = table_data.find("dt", string="Exterior Color")
        color = color_attribute.find_next("dd").text if color_attribute else ""

        # Find drivetrain
        drive_attribute = table_data.find("dt", string="Drivetrain")
        drive = drive_attribute.find_next("dd").text if drive_attribute else ""

        # Find engine
        engine_attribute = table_data.find("dt", string="Engine")
        engine = engine_attribute.find_next("dd").text if engine_attribute else ""

        # Find transmission
        transmission_attribute = table_data.find("dt", string="Transmission")
        transmission = transmission_attribute.find_next("dd").text if transmission_attribute else ""

        return (make, model, vin, body_style, color, drive, engine, transmission)

    def location_details(self, table_data):
        """
        This will get the location details of the bid
        """
        # Find location
        location_attribute = table_data.find("dt", string="Location")
        if location_attribute:
            location = location_attribute.find_next("dd").text
            pattern = r'[0-9]{4,}'
            location_zip4 = " ".join(re.findall(pattern, location))
            location_zip5 = location_zip4
            location_state = " ".join(re.findall(r'\b[A-Z]{2}\b', location))
            location_city = location.split(location_state)[0].strip()
            location_country = ""
        else:
            location_zip4 = location_city = location_state = location_country = location_zip5 = ""

        return (location_zip4, location_city, location_state, location_country, location_zip5)

    def image_details(self, soup_text):
        """
        Get the thumbnail image link and all other images
        link
        """
        # Find image thumbnail
        div_tag = soup_text.find('div', class_=("preload-wrap", "main loaded"))
        img_tag = div_tag.find('img')
        image_thumbnail = img_tag['src'] if img_tag else ""

        all_images_url = []
        exterior_images = soup_text.find("div", class_= ("group exterior"))
        ext_images_div = exterior_images.find_all("div", class_= ("preload-wrap"," loaded"))
        for img in ext_images_div:
            all_images_url.append(img.find("img")['src'])

        interior_images = soup_text.find("div", class_= ("group interior"))
        int_images_div = interior_images.find_all("div", class_= ("preload-wrap"," loaded"))
        for img in int_images_div:
            all_images_url.append(img.find("img")['src'])

        images = ", ".join(all_images_url)

        return (image_thumbnail, images)

if __name__ == "__main__":
    time1 = time.time()

    obj = CarsAndBids()
    obj.create_empty_csv()
    obj.create_driver()
    obj.get_vehicle_url()
    obj.get_vehicle_data()

    print(f"Time Taken to get the data is {time1 - time.time()} seconds")

