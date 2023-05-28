import os
import csv
import json
import datetime
import time
from requests import Session
from config import variables


class Autoauctionmall:

    def __init__(self):
        """
        To initialize some values
        """
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(self.script_dir)

        self._autoauction_session = Session()
        self.total = 0
        self.data = []

        cwd = os.path.abspath(os.getcwd())
        self.folder_name = os.path.join(cwd, 'Output_folder',
                            datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S'))

    @staticmethod
    def __make_data_filters__(**kwargs) -> dict:
        """
        Filter data from the url
        """
        page = kwargs.get("page")
        from_year = kwargs.get("from_year")
        to_year = kwargs.get("to_year")
        old_params = variables.get("params", {})
        params_data = variables.get("data", {})
        new_params = old_params.format(page=page, from_year=from_year, to_year=to_year)
        params_data['requests'][0]['params'] = new_params
        return params_data

    def __get_data__(self) -> None:
        """
        Making request to api for the data
        """
        total_page = 0
        page = 0
        url = variables.get("api-url", "")
        while 1:
            data = self.__make_data_filters__(
                page=page,
                from_year=1970,
                to_year=2023)
            response = self._autoauction_session.post(
                url,
                headers=variables.get("headers", {}),
                data=json.dumps(data),
            )
            if response.ok:
                json_data = response.json().get("results", "")
                if json_data:
                    data = json_data[0]
                    cars = data.get("hits")
                    total_page = data.get("nbPages")
                    print(len(cars), "cars")
                    for car in cars:
                        self.data.append(self.data_formating(car))
                        self.total += 1
                    print(f"page : {page + 1}/{total_page}")
            else:
                print(response.content)
            page += 1
            if page == total_page:
                break
            time.sleep(2)

    @staticmethod
    def data_formating(car: dict) -> tuple:
        """
        formatting the data so that it could be saved to csv
        """
        image_url = car.get('image', '')
        image_thumbnail = image_url
        date_time = datetime.datetime.strptime(car.get('start_date', ''), '%Y-%m-%dT%H:%M:%S.%fZ') \
            if car.get('start_date', '') else ''
        sale_date = date_time.date() if car.get('start_date') else ''
        day_of_week = date_time.strftime('%A')
        sale_time = str(date_time.time()) if car.get('start_date') else ''
        odometer = car.get('odometer', '')
        buy_it_now_price = car.get('buyNow') if car.get('buyNow') else ''
        high_bid_non_vix_sealed_vix = car.get('current_bid') if car.get('current_bid') else ''
        others = car.get('_highlightResult', '')
        year = others.get('year').get('value', '')
        make = others.get('make').get('name').get('value', '')
        model_group = others.get('model').get('name').get('value', '')
        location_city = others.get('city').get('value', '')
        location_state = others.get('fullState', '').get('value', '')
        color = others.get('color').get('value', '')
        vin = others.get('vin').get('value', '')
        yard_number = ''
        yard_name = ''
        item = car.get('name', '')
        Iot_number = ''
        body_style = ''
        vehical_type = ''
        model_detail = ''
        time_zone = ''
        damage_description = ''
        secondary_damage = ''
        sale_title_state = ''
        sale_title_type = ''
        has_keys = ''
        Iot_cord_code = ''
        odometer_brand = ''
        est_retail_value = ''
        repair_cost = ''
        engine = ''
        drive = ''
        transmission = ''
        fuel_type = ''
        cylinders = ''
        runs_drives = ''
        sale_status = ''
        special_note = ''
        location_zip5 = ''
        location_zip4 = ''
        currency_code = ''
        location_country = ''
        create_date_time = ''
        grid_row = ''
        make_an_offer_eligible = ''
        trim = ''
        last_updated_time = ''
        rentals = ''
        copart_select = ''
        source = ''

        return yard_number, yard_name, sale_date, day_of_week, sale_time, \
               time_zone, item, Iot_number, vehical_type, year, make, model_group, \
               model_detail, body_style, color, damage_description, secondary_damage, \
               sale_title_state, sale_title_type, has_keys, Iot_cord_code, vin, odometer, \
               odometer_brand, est_retail_value, repair_cost, engine, drive, transmission, \
               fuel_type, cylinders, runs_drives, sale_status, high_bid_non_vix_sealed_vix, \
               special_note, location_city, location_state, location_zip5, location_zip4, \
               location_country, currency_code, image_thumbnail, create_date_time, grid_row, \
               make_an_offer_eligible, buy_it_now_price, image_url, trim, last_updated_time, \
               rentals, copart_select, source

    def make_csv(self) -> None:
        """
        Making a csv
        """
        headers = [
            'Yard_number',
            'Yard_name',
            'Sale_date',
            'Day_of_week',
            'Sale_time',
            'Time_zone',
            'Item',
            'Iot_number',
            'Vehical_type',
            'Year',
            'Make',
            'Model_group',
            'Model_detail',
            'Body_style',
            'Color',
            'Damage_description',
            'Secondary_damage',
            'Sale_title_state',
            'Sale_title_type',
            'Has_keys',
            'Iot_cord_code',
            'Vin',
            'Odometer',
            'Odometer_brand',
            'Est_retail_value',
            'Repair_cost',
            'Engine',
            'Drive',
            'Transmission',
            'Fuel_type',
            'Cylinders',
            'Runs_drives',
            'Sale_status',
            'High_bid_non_vix_sealed_vix',
            'Special_note',
            'Location_city',
            'Location_state',
            'Location_zip5',
            'Location_zip4',
            'Location_country',
            'Currency_code',
            'Image_thumbnail',
            'Create_date_time',
            'Grid_row',
            'Make_an_offer_eligible',
            'Buy_it_now_price',
            'Image_url',
            'Trim',
            'Last_updated_time',
            'Rentals',
            'Copart_select',
            'Source'
        ]
        if self.data:
            if not os.path.exists(self.folder_name):
                os.makedirs(self.folder_name)
            with open(f"{self.folder_name}/autoauction_csv.csv", "w", encoding="utf-8") as fl:
                csv_out = csv.writer(fl)
                csv_out.writerow(headers)
                for row in self.data:
                    csv_out.writerow(row)
            print("saved to csv")

    def start(self):
        self.__get_data__()
        self._autoauction_session.close()


if __name__ == "__main__":
    autoauction = Autoauctionmall()
    autoauction.start()
    print(f"Total {autoauction.total} cars")
    autoauction.make_csv()
