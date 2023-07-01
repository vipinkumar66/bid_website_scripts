"""
Import Required Libraries
"""
import csv
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import requests
from bs4 import BeautifulSoup


class Abetter:
    """
    Created a Salvagebid class to scrape data from its
    website and stored it into CSV
    """

    def __init__(self):
        """
        Initialised the variable and created the csv name salvagebid
        """
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(self.script_dir)


        self.headers = {
            'authority': 'abetter.bid',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                      'image/webp,image/apng,*/*;q=0.8,application/'
                      'signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'sec-ch-ua': '"Microsoft Edge";v="111", "Not(A:Brand";v="8", '
                         '"Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 '
                          'Edg/111.0.1661.62',
        }
        self.writer = None
        cwd = os.path.abspath(os.getcwd())
        self.folder_name = os.path.join(cwd, 'Output_folder',
                            datetime.now().strftime('%Y-%m-%d_%H_%M_%S'))

    def create_empty_csv(self):
        """
        Write a column name for csv and execute the code
        with multi-threading to get response
        :return writer
        """
        if not os.path.exists(self.folder_name):
            os.makedirs(self.folder_name)
        with open(f"{self.folder_name}/abetter.csv", mode='a',
                  newline='', encoding='utf-8') as csv_file:
            self.writer = csv.writer(csv_file)
            self.writer.writerow(
                ['yard_number', 'yard_name', 'sale_date', 'day_of_week', 'sale_time', 'time_zone', 'item',
                 'lot_number', 'vehicle_type', 'year', 'make', 'model_group', 'model_detail', 'body_style', 'color',
                 'damage_description', 'secondary_damage', 'sale_title_state', 'sale_title_type', 'has_keys',
                 'lot_cond_code', 'vin', 'odometer', 'odometer_brand', 'est_retail_value', 'repair_cost', 'engine',
                 'drive', 'transmission', 'fuel_type', 'cylinders', 'runs_drives', 'sale_status',
                 'high_bid_non_vix_sealed_vix',
                 'special_note', 'location_city', 'location_state', 'location_zip5', 'location_zip4',
                 'location_country', 'currency_code', 'image_thumbnail', 'create_date_time', 'grid_row',
                 'make_an_offer_eligible', 'buy_it_now_price', 'image_url', 'trim', 'last_updated_time', 'rentals',
                 'copart_select', 'source', 'Timestamp']
            )

            with ThreadPoolExecutor() as exe:
                exe.map(self.get_all_links, range(1, 281))

    def get_all_links(self, page_no):
        """
        Get all links of cars to get detail data
        :param page_no: pagination to get all page data
        """
        today_date = datetime.today()
        formatted_date = today_date.strftime("%m-%d-%Y")
        response = requests.get(f'https://abetter.bid/en/car-finder/sale-date-{formatted_date}-to-{formatted_date}/page-{page_no}',
                                headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        find_div = soup.find_all('div', class_='swiper-wrapper')
        for one_div in find_div:
            all_links.append(one_div.find('a').get('href'))
        print(f"Total Links: {len(all_links)}")

    def get_response(self, link):
        """
        Getting all required data from response and stored that into CSV
        :param link: Taking one by one link of car data
        """
        cookies = {
            'initialTrafficSource': 'utmcsr=(direct)|utmcmd=(none)|utmccn=(not set)',
            '__utmzzses': '1',
            '_gcl_au': '1.1.669249620.1683789216',
            '_gid': 'GA1.2.1679668295.1683789216',
            'roistat_visit': '1579205',
            'roistat_first_visit': '1579205',
            'roistat_visit_cookie_expire': '1209600',
            '_hjFirstSeen': '1',
            '_hjIncludedInSessionSample_1292130': '0',
            '_hjSession_1292130': 'eyJpZCI6IjdiZGU3M2VlLWVkYWEtNGY5NC04MDRjLTYyY'
                                  'WQyYjRiMGQ5NyIsImNyZWF0ZWQiOjE2ODM3ODkyMTczNTM'
                                  'sImluU2FtcGxlIjpmYWxzZX0=',
            '_hjAbsoluteSessionInProgress': '0',
            '_hjHasCachedUserAttributes': 'true',
            '_fbp': 'fb.1.1683789217562.763017224',
            '___dc': 'edf5c9d4-8c2f-44f9-b777-8db567c2aac9',
            'g_state': '{"i_p":1683796421317,"i_l":1}',
            'intercom-device-id-yhv9hs5c': '5257d472-42c3-4a42-8d19-2bd39520768a',
            '_hjSessionUser_1292130': 'eyJpZCI6IjJiNGY3MWFjLWEzNzAtNTFkYi04NjQ4LT'
                                      'gzZjk4NmM2MThjNyIsImNyZWF0ZWQiOjE2ODM3ODky'
                                      'MTczNDQsImV4aXN0aW5nIjp0cnVlfQ==',
            'roistat_call_tracking': '0',
            'roistat_emailtracking_email': 'null',
            'roistat_emailtracking_tracking_email': 'null',
            'roistat_emailtracking_emails': '%5B%5D',
            'roistat_cookies_to_resave': 'roistat_ab%2Croistat_ab_submit%2Croistat_'
                                         'visit%2Croistat_call_tracking%2Croistat_'
                                         'emailtracking_email%2Croistat_emailtracking'
                                         '_tracking_email%2Croistat_emailtracking_emails',
            'PHPSESSID': 'qvtvl3delo7l44gp8m0qkcjjei',
            'b244bbd6933027147a51583efe3fda69': 'e249ce95f1f76fc8e019944d30d200d1cf61bc'
                                                '86a%3A4%3A%7Bi%3A0%3Bs%3A6%3A%22610997'
                                                '%22%3Bi%3A1%3Bs%3A4%3A%22Zeal%22%3Bi%3A'
                                                '2%3Bi%3A864000%3Bi%3A3%3Ba%3A0%3A%7B%7D%7D',
            'intercom-id-yhv9hs5c': '285d4848-8042-4638-abf7-2f469fbf5c1b',
            '__stripe_mid': '494173e2-6d43-4240-a0f3-8e3db85b258e6f293d',
            '__stripe_sid': '0e400c59-9a24-4177-9608-3e5df14673f7e756df',
            'recently_viewed': 'MzcyMDQyODMsMzczMTM4MDMsMzczNzAzMDMsMzc2MTM5MjMsNDExNzIxNz'
                               'MsMzY0NjQ1MTMsNDQzMTY5MjMsNDQzNTMwNjMsNDQzMzk5ODMsNDQ1ODcwNTM%3D',
            'd_cy': 'US',
            'd_z': '07101',
            'd_zd': 'Newark%2C+NJ',
            '_ga': 'GA1.2.873730882.1683789216',
            '_uetsid': '59388e60efcb11eda61037e0cb8edd02',
            '_uetvid': '59390210efcb11ed95352d6034e62713',
            'intercom-session-yhv9hs5c': 'VE5sTVp3QisvOVN6Z3pCdmRCd1BYMHNUTDZSOG1lYlU0YWNLS'
                                         'zlac1RXR0NZRHZmTTZiVXBMbXNrRVdtQnE0Ni0tWUZxbE9Xa3'
                                         'Z6TnI3NzA4ZTkzcjg1Zz09--9fb980a94f415c5c8371a62cc'
                                         '37612579014313a',
            '__language': 'en',
            'search_params': 'search_type%3Dcar-finder%26searchParams%3Dtype-automobiles'
                             '%252Fyear-1919-2024%26page%3D2',
            '_ga_PZDDMGXFXX': 'GS1.1.1683789217.1.1.1683790250.8.0.0',
        }

        headers = {
            'authority': 'abetter.bid',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                      'image/avif,image/webp,image/apng,*/*;q=0.8,application/'
                      'signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/112.0.0.0 Safari/537.36',
        }

        params = {
            'search_hash': '5310163988bf31cb43288b2fb6fa30a1',
        }

        response2 = requests.get(
            f'{link}',
            params=params,
            cookies=cookies,
            headers=headers,
        )
        content = BeautifulSoup(response2.content, 'html.parser')

        try:
            vin = content.find('a', class_='copy__text copy__text--hover '
                                           'details__epicvin js-click-epicvin').get_text().strip()
        except IndexError:
            vin = ""
        try:
            lot = content.find('div', class_='copy__text').get_text()
        except IndexError:
            lot = ""
        try:
            current_bid = content.find('div', class_='lot-form-item__value '
                                                     'lot-form-item__value--price '
                                                     'js-lot-current-bid').get_text().strip()
        except IndexError:
            current_bid = ""

        script = content.find_all('script')[8].get_text()
        script_json = json.loads(script)
        try:
            odometer = script_json['mileageFromOdometer']
        except IndexError:
            odometer = ""
        try:
            title = script_json['name']
            make = str(title).split(" ")[1]
        except IndexError:
            make = ""
        try:
            color = script_json['color']
        except IndexError:
            color = ""
        try:
            fuel_type = script_json['fuelType']
        except IndexError:
            fuel_type = ""
        try:
            model = script_json['model']
        except IndexError:
            model = ""
        try:
            production_year = script_json['productionDate']
        except IndexError:
            production_year = ""
        try:
            vehicle_transmission = script_json['vehicleTransmission']
        except IndexError:
            vehicle_transmission = ""
        try:
            engine_displacement = script_json['vehicleEngine']['engineDisplacement']
        except IndexError:
            engine_displacement = ""
        try:
            images = script_json['image']
        except IndexError:
            images = ""

        timestamp = datetime.now()
        yard_number = ""
        yard_name = ""
        try:
            sale_date = content.find("div", class_="lot-live-bid__title lot-live-bid__title--upcoming").get_text().strip()
        except:
            sale_date = ""
        day_of_week = ""
        try:
            sale_time = content.find_all("div", class_="details-item__text")[29].get_text().strip()
        except:
            sale_time = ""
        try:
            vehicle_type = content.find_all("div", class_="details-item__text details-item__text--line"
                                            )[6].get_text().strip()
        except:
            vehicle_type = ""
        time_zone = ""
        item = ""
        body_style = ""
        model_details = ""
        damage_description = ""
        try:
            secondary_damage = content.find_all("div", class_="details-item__text details-item__text--line"
                                                )[3].get_text().strip()
        except:
            secondary_damage = ""
        location_zip5 = ""
        location_zip4 = ""
        location_country = "USA"
        currency_code = "$"
        try:
            image_thumbnail = images[0]
        except:
            image_thumbnail = ""
        create_date_time = ""
        try:
            grid_row = content.find_all("div", class_="details-item__text")[31].get_text().strip()
        except:
            grid_row = ""
        try:
            buy_it_now_price = content.find("span", class_="buy-now-block__price").get_text().strip()
        except:
            buy_it_now_price = ""
        trim = ""
        try:
            last_updated_time = content.find("div", class_="lot-live-banner__body")[32].get_text().strip()
        except:
            last_updated_time = ""
        rentals = "A better Bid Car Auction"
        copart_select = "A better Bid Car Auction"
        sale_title_state = ""
        sale_title_type = ""
        has_keys = ""
        lot_cond_code = ""
        odometer_brand = ""
        est_retail_value = ""
        repair_cost = ""
        try:
            drive = script_json['driveWheelConfiguration']
        except:
            drive = ""
        try:
            cylinders = script_json['vehicleEngine']['engineDisplacement']
        except:
            cylinders = ""
        runs_drives = ""
        sale_status = ""
        high_bid_non_vix_sealed_vix = ""
        special_note = ""
        try:
            location_city = content.find("div", class_="details-item__text--blue details-item__text-bold"
                                         ).get_text().strip().split(",")[0]
        except:
            location_city = ""
        try:
            location_state = content.find("div", class_="details-item__text--blue details-item__text-bold"
                                          ).get_text().strip().split(",")[1].strip()
        except:
            location_state = ""
        source = ""

        with open(f"{self.folder_name}/abetter.csv", mode='a',
                  newline='', encoding='utf-8') as csv_file:
            self.writer = csv.writer(csv_file)
            self.writer.writerow(
                [ yard_number, yard_name, sale_date, day_of_week, sale_time, time_zone, item, lot,
                 vehicle_type, production_year, make, model, model_details, body_style, color, damage_description,
                 secondary_damage, sale_title_state, sale_title_type, has_keys, lot_cond_code, vin, odometer,
                 odometer_brand, est_retail_value, repair_cost, engine_displacement, drive, vehicle_transmission,
                 fuel_type, cylinders, runs_drives, sale_status, high_bid_non_vix_sealed_vix, special_note,
                 location_city, location_state, location_zip5, location_zip4, location_country, currency_code,
                 image_thumbnail, create_date_time, grid_row, current_bid, buy_it_now_price, images, trim,
                 last_updated_time, rentals, copart_select, source, timestamp]
            )


start_time = time.time()

all_links = []
abetter = Abetter()
abetter.create_empty_csv()
with ThreadPoolExecutor() as exe_link:
    exe_link.map(abetter.get_response, all_links)

end_time = time.time()
print(f"Total running time: {end_time - start_time} seconds")
