"""
Imported a required Libraries
"""
import os
import csv
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import requests


class Salvagebid:
    """
    Created a Salvagebid class to scrape data from it is website and stored it into CSV
    """

    def __init__(self):
        """
        Initialised the variable and created the csv name salvagebid
        """
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(self.script_dir)

        cwd = os.path.abspath(os.getcwd())
        self.folder_path = os.path.join(cwd, 'Output_Folder', datetime.now().strftime('%Y-%m-%d_%H_%M_%S'))

        self.writer = None
        self.headers = {
            'authority': 'www.salvagebid.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'sec-ch-ua': '"Microsoft Edge";v="111", '
                         '"Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 '
                          'Edg/111.0.1661.62',
        }

    def create_empty_csv(self):
        """
        Write a column name for csv and execute the code with multi-threading to get response
        """
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)

        with open(f"{self.folder_path}/salvagebid.csv", mode='a',
                  newline='', encoding='utf-8') as csv_file:

            self.writer = csv.writer(csv_file)
            self.writer.writerow(
                ['id', 'yard_number', 'yard_name', 'sale_date', 'day_of_week', 'sale_time', 'time_zone', 'item',
                 'lot_number', 'vehicle_type', 'year', 'make', 'model_group', 'model_detail', 'body_style', 'color',
                 'damage_description', 'secondary_damage', 'sale_title_state', 'sale_title_type', 'has_keys',
                 'lot_cond_code', 'vin', 'odometer', 'odometer_brand', 'est_retail_value', 'repair_cost', 'engine',
                 'drive', 'transmission', 'fuel_type', 'cylinders', 'runs_drives', 'sale_status',
                 'high_bid_non_vix_sealed_vix',
                 'special_note', 'location_city', 'location_state', 'location_zip5', 'location_zip4',
                 'location_country', 'currency_code', 'image_thumbnail', 'create_date_time', 'grid_row',
                 'make_an_offer_eligible', 'buy_it_now_price', 'image_url', 'trim', 'last_updated_time', 'rentals',
                 'copart_select', 'source', 'Link', 'Timestamp']
            )
            with ThreadPoolExecutor() as exe1:
                exe1.map(self.get_response, range(1, 386))

    def get_response(self, page_no):
        """
        Requesting the response and getting that data and
        call get_data to get data
        :param page_no: taken from 1 to 386
        """

        response = requests.get(
            f'https://www.salvagebid.com/rest-api/v1.0/lots/search?page={page_no}'
            f'&per_page=26&type=car&make=*&model=*&search_id=&search_query=&'
            f'year_from=2022&year_to=2023&sort_field=&sort_order=&sales_type=*&'
            f'distance=*&destination_zip=&location_state=*&location_city=*&'
            f'primary_damage=*&loss_type=*&title_name=*&exterior_color=*&'
            f'odometer_min=*&odometer_max=*',
            headers=self.headers,
        )

        lots = response.json()['lots']

        for lot in lots:
            self.get_data(lot)

    def get_data(self, one_lot):
        """
        Getting the data as per column name like ID, Car model, VIN, etc...
        And stored that into csv as a row
        :param one_lot: take one car detail data
        """

        try:
            main_id = one_lot['id']
        except KeyError:
            main_id = ""

        try:
            vin = one_lot['VIN']
        except KeyError:
            vin = ""

        try:
            vehicle_name = one_lot['vehicle_name']
        except KeyError:
            vehicle_name = ""

        try:
            vehicle_type = one_lot['vehicle_type']
        except KeyError:
            vehicle_type = ""

        try:
            auction_in_progress = one_lot['auction_in_progress']
        except KeyError:
            auction_in_progress = ""

        try:
            auction_type_str = one_lot['auction_type_str']
        except KeyError:
            auction_type_str = ""

        try:
            sale_date = one_lot['sale_date']
        except KeyError:
            sale_date = ""

        try:
            retail_value = one_lot['retail_value']
        except KeyError:
            retail_value = ""

        try:
            repair_cost = one_lot['repair_cost']
        except KeyError:
            repair_cost = ""

        try:
            current_bid_value = one_lot['current_bid_value']
        except KeyError:
            current_bid_value = ""

        try:
            odometer_status = one_lot['odometer_status']
        except KeyError:
            odometer_status = ""

        try:
            odometer_value = one_lot['odometer_value']
        except KeyError:
            odometer_value = ""

        try:
            damage = one_lot['damage']
        except KeyError:
            damage = ""

        try:
            color = one_lot['color']
        except KeyError:
            color = ""

        try:
            location_state = one_lot['location_state']
        except KeyError:
            location_state = ""

        try:
            location_city = one_lot['location_city']
        except KeyError:
            location_city = ""

        try:
            body_style = one_lot['body_style']
        except KeyError:
            body_style = ""

        try:
            doc_type = one_lot['doc_type']
        except KeyError:
            doc_type = ""

        try:
            images = one_lot['images']
        except KeyError:
            images = ""

        try:
            link = f'https://www.salvagebid.com/{one_lot["id"]}-' \
                   f'{one_lot["vehicle_name"].replace(" ", "-").lower()}'
        except KeyError:
            link = ""

        timestamp = datetime.now()
        yard_number = ""
        yard_name = ""
        day_of_week = ""
        sale_time = ""
        time_zone = ""
        lot_number = ""
        year = vehicle_name.split(" ")[0]
        make = vehicle_name.split(" ")[1]
        model_group = ""
        model_detail = ""
        item = ""
        secondary_damage = ""
        try:
            sale_title_state = one_lot['title_state']
        except:
            sale_title_state = ""
        sale_title_type = ""
        has_keys = ""
        lot_cond_code = ""
        odometer_brand = ""
        engine = ""
        drive = ""
        transmission = ""
        fuel_type = ""
        cylinders = ""
        runs_drives = ""
        try:
            sale_status = one_lot['bid_status']
        except:
            sale_status = ""
        high_bid_non_vix_sealed_vix = ""
        special_note = ""
        location_zip5 = ""
        location_zip4 = ""
        location_country = "USA"
        currency_code = "$"
        create_date_time = ""
        grid_row = ""
        source = ""
        try:
            buy_it_now = one_lot['buy_it_now']
        except:
            buy_it_now = ""
        trim = ""
        last_updated_time = ""
        rentals = ""
        copart_select = ""

        self.writer.writerow(
            [main_id, yard_number, yard_name, sale_date, day_of_week, sale_time, time_zone, item,
             lot_number, vehicle_type, year, make, model_group, model_detail, body_style, color,
             damage, secondary_damage, sale_title_state, sale_title_type, has_keys, lot_cond_code,
             vin, odometer_value, odometer_brand, retail_value, repair_cost, engine, drive, transmission,
             fuel_type, cylinders, runs_drives, sale_status, high_bid_non_vix_sealed_vix, special_note,
             location_city, location_state, location_zip5, location_zip4, location_country, currency_code,
             images[0], create_date_time, grid_row, current_bid_value, buy_it_now, images, trim,
             last_updated_time, rentals, copart_select, source, link, timestamp]
        )


start_time = time.time()

salvagebid = Salvagebid()
salvagebid.create_empty_csv()

end_time = time.time()
print(f"Total running time: {end_time - start_time} seconds")
