"""Module to extract the auctions' data from Capital Auto Auction Website"""
# Importing Required Libraries
import os
from concurrent.futures import ThreadPoolExecutor
import datetime
from time import time
from functools import wraps
import math
import requests
import pandas as pd
from bs4 import BeautifulSoup


class CapitalAutoAuction:
    """Extracts the data of car's auctions from Capital Auto Auction Website"""
    def __init__(self):
        self.all_links = []
        current_folder_path = os.getcwd()
        output_folder_name = datetime.datetime.now().strftime('%H_%M_%S')
        absolute_path = os.path.abspath(os.path.join(current_folder_path,
                        f"Capital_auto_auction_{output_folder_name}"))
        self.current_folder_path = absolute_path
        if not os.path.exists(self.current_folder_path):
            os.makedirs(self.current_folder_path)
        self.master_json = {"Title": [] , "VIN": [], "Stock#": [], "Year": [],
                            "Type": [], "Drive": [], "Engine": [], "Transmission": [],
                            "Ext color": [], "Make": [], "Model": [], "Trim": [],
                            "Odo": [], "Location": [], "Live Start": [],"currency_code":[],
                            "ENGINE": [], "lot_cond_code":[], "fuel_type":[],"BODY": [],
                            "KEYS": [],"image_thumbnail":[],"CYLINDER": [],
                            "yard_number":[], "yard_name":[],"day_of_week":[], "sale_time":[],
                            "time_zone":[],"model_details":[], "damage_description":[],
                            "secondary_damage":[], "sale_title_state":[], "sale_title_type":[],
                            "odometer_brand":[], "est_retail_value":[], "repair_cost":[],
                            "runs_drives":[], "sale_status":[],
                            "high_bid_non_vix_sealed_vix":[], "special_note":[],
                            "location_state":[], "location_zip5":[], "location_zip4":[],
                            "location_country":[],"create_date_time":[], "grid_row":[],
                            "current_bid":[], "buy_it_now_price":[], "images":[], "trim":[],
                            "last_updated_time":[], "rentals":[], "copart_select":[], "source":[],
                            "Time_Stamp": []}

    @staticmethod
    def execution_time(function):
        """ use this decorator for execution time of any function"""
        if "function" not in str(type(function)):
            return None

        @wraps(function)
        def wrapper(*args, **kwargs):

            start = time()
            print(f"function named '{function.__name__}' started")
            result = function(*args, **kwargs)
            seconds = time() - start
            print(seconds, "seconds")
            if seconds <= 60:
                print(seconds, "seconds")
            elif 60 < seconds <= 3600:
                print(seconds / 60, "minutes")
            elif 3600 < seconds <= 86400:
                print((seconds / 60) / 60, "hrs")
            elif seconds > 86400:
                print(((seconds / 60) / 60) / 24, "day")
            return result

        return wrapper

    def get_links(self):
        """Scraps all the links of data and returns the list of these links"""

        # for getting data count
        headers = {
            'authority': 'www.capitalautoauction.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.7',
            'referer': 'https://www.capitalautoauction.com/inventory?per_page=100',
            'sec-ch-ua': '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'x-csrf-token': 'fjP862XQQrrqyHkXb7eHIe7LBcvHbyvAxXVwbyN6',
            'x-requested-with': 'XMLHttpRequest',
            'x-xsrf-token': 'eyJpdiI6InpTK21YTi9sY2lxWHBqOXpvRXBsT3c9PSIsInZhbHVlIjoiRVo2dFMvWEI4a'
                            '0wyVEd2N0hrZEY2blE4U0NyMmx5bGtQbThJellHaXdra0w0Q2hFUlRnYjBEenAzUUl4L1'
                            'htc200UnZab3JiUzBqRVRVWVVrb3UzY1NJcWljNThvZjJWQndQaVRFTnN1K3A0ZVg2bHF'
                            'CSG9nN25mMzNIcWorWlYiLCJtYWMiOiJlNGM4NmJhMDFmMTk0MDZlMGNmYTIwMjZjYWJk'
                            'MjM3NjE5MDQ1YmE3Yzg4M2I4YjExYjk4ZmIyY2NjMzI5NThjIiwidGFnIjoiIn0=',
        }
        params = {
            'scope': 'client',
        }
        url = 'https://www.capitalautoauction.com/api-internal/inventory/filter-values'
        response = requests.get(url, params=params, headers=headers, timeout=10)
        data_count = response.json()['countSelect']
        pages = math.ceil(data_count/100)

        for page in range(1, pages+1):
            link_response = requests.get('https://www.capitalautoauction.com/inventory', params={
                'per_page': '100',
                'sort': 'make',
                'sort_direction': '',
                'page': f'{page}',
            }, headers={
                'authority': 'www.capitalautoauction.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,'
                          'image/webp,image/apng,*/*;q=0.8',
                'accept-language': 'en-US,en;q=0.9',
                'cache-control': 'max-age=0',
                'referer': f'https://www.capitalautoauction.com/inventory?per_page=100'
                           f'&sort=make&page={page}',
                'sec-ch-ua': '"Brave";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'sec-gpc': '1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                              ' (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            }, timeout=10)
            soup = BeautifulSoup(link_response.text, 'html.parser')
            all_cards = soup.find_all('div', class_='catalog__card')
            self.all_links += [card.select('div.card__buttons a.card__button-detailes')
                               [0].get('href') for card in all_cards]

        return self.all_links

    def get_data_from_link(self, link):
        """Gets the Values of 100+ pre-defined Parameters using the link of the web page given."""

        headers = {
            'authority': 'www.capitalautoauction.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,'
                      'image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'en-US,en;q=0.7',
            'cache-control': 'max-age=0',
            'referer': 'https://www.capitalautoauction.com/inventory?per_page=100',
            'sec-ch-ua': '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'sec-gpc': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        }
        soup = BeautifulSoup(requests.get(link, headers=headers, timeout=10).text, 'html.parser')
        title = ' '.join([i for i in soup.select('h1.vehicle__title')[0].text.strip()
                         .replace('\n', '').split(' ') if i != ""])

        image_div = soup.find("div", class_="slideshow__photo_carousel ")
        image = image_div.find("img")
        if image:
            image_url = image['src']
        else:
            image_url = ""

        current_bid = soup.find("div", class_="vehicle__bid")
        if current_bid:
            current_bid = current_bid.text
        else:
            current_bid = ""

        json_to_add = {"Title": title , "VIN": "", "Stock#": "", "Year": "",
                        "Type": "", "Drive": "", "Engine": "", "Transmission": "",
                        "Ext color": "", "Make": "", "Model": "", "Trim": "",
                        "Odo": "", "Location": "", "Live Start": "","currency_code":"",
                        "ENGINE": "", "lot_cond_code":"", "fuel_type":"","BODY": "",
                        "KEYS": "","image_thumbnail":image_url,"CYLINDER": "",
                        "yard_number":"", "yard_name":"","day_of_week":"", "sale_time":"",
                        "time_zone":"","model_details":"", "damage_description":"",
                        "secondary_damage":"", "sale_title_state":"", "sale_title_type":"",
                        "odometer_brand":"", "est_retail_value":"", "repair_cost":"",
                        "runs_drives":"", "sale_status":"",
                        "high_bid_non_vix_sealed_vix":"", "special_note":"",
                        "location_state":"", "location_zip5":"", "location_zip4":"",
                        "location_country":"","create_date_time":"", "grid_row":"",
                        "current_bid":current_bid, "buy_it_now_price":"", "images":"", "trim":"",
                        "last_updated_time":"", "rentals":"", "copart_select":"", "source":"",
                        "Time_Stamp": str(datetime.datetime.now())}

        # main parameters
        option_labels = [i.select('span.options__label')[0].text.strip().replace(':', '') for i in
                         soup.select('li.options__item') if i.select('span.options__label') != []]
        options_value = [i.select('span.options__value')[0].text.strip() for i in
                         soup.select('li.options__item') if i.select('span.options__label') != []]
        for counter in range(len(option_labels)):
            if option_labels[counter] in self.master_json:
                json_to_add[option_labels[counter]] += options_value[counter]

        # condition report parameters
        condition_reports = [[j.text for j in i.select('span.options__value--unbold')] for i in
                             soup.select('li.options__item') if
                             i.select('span.options__value--unbold') != []]
        condition_reports = [element for innerList in condition_reports for element in innerList]

        cr_labels = [i.split(':')[0].strip() for i in condition_reports if ':' in i]
        cr_values = [i.split(':')[1].strip() for i in condition_reports if ':' in i]
        for cr_counter in range(len(cr_labels)):
            if cr_labels[cr_counter] in self.master_json:
                json_to_add[cr_labels[cr_counter]] += cr_values[cr_counter]
                print(json_to_add)

        # Appending the data into main data (master_json)
        for data in json_to_add:
            self.master_json[data].append(json_to_add[data])


    @execution_time
    def scrap_data(self):
        """Scraps the entire data from website using multithreading"""
        with ThreadPoolExecutor() as executor:
            executor.map(self.get_data_from_link, self.get_links())
        dataframe = pd.DataFrame(self.master_json)
        dataframe.to_csv(f'{self.current_folder_path}/Capital Auto Auction Data.csv',
                         index=False)


if __name__ == "__main__":
    try:
        caa_obj = CapitalAutoAuction()
        caa_obj.scrap_data()
    except Exception:
        print(Exception)

# Took 251 seconds (4.18 mins) to execute