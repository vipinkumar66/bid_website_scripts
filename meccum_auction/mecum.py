"""Module to extract the bids' data from Mecum Website"""
# Importing Required Libraries
import time
from functools import wraps
from urllib import parse
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
import csv
import json
import requests
from bs4 import BeautifulSoup as bs
from config import (folder_name, auction_url,
                    auction_data_headers, headers)


class MecumAuctions:
    """Extracts the data of Bids from Mecum Bids Website"""
    def __init__(self):
        self.session = requests.session()
        with open(f"{folder_name}/meccum_data.csv", "w", encoding="utf-8") as file_:
            writer = csv.writer(file_)
            writer.writerow(headers)

    @staticmethod
    def execution_time(function):
        """ use this decorator for execution time of any function"""
        if "function" not in str(type(function)):
            return None

        @wraps(function)
        def wrapper(*args, **kwargs):
            start = time.time()
            print(f"function named '{function.__name__}' started")
            result = function(*args, **kwargs)
            seconds = time.time() - start
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

    def get_auction_names(self):
        """Extract all the auction names to be extracted from the website and returns the
         list of auction names."""
        auctions_response = requests.get(auction_url, timeout=10)
        auctions_data = auctions_response.json()['data']['auctions']['edges']
        auctions_names = []
        today = datetime.today()
        month_name = today.strftime('%B')

        for auc in auctions_data:
            if month_name in auc['node']['auctionFields']['auctionEndDate']:
                auc_title = auc['node']['title']
                auc_start_date = datetime.strptime(auc['node']['auctionFields']['auctionStartDate'],
                                                '%B %d, %Y')
                auc_end_date = datetime.strptime(auc['node']['auctionFields']['auctionEndDate'],
                                                '%B %d, %Y')
                auc_string = f"{auc_title}|{int(time.mktime(auc_start_date.timetuple()))}|" \
                            f"{int(time.mktime(auc_end_date.timetuple()))}"
                auctions_names.append(auc_string)
            else:
                pass
        print(auctions_names)
        return auctions_names

    def get_auction_data(self, auction_name):
        """Extract the data of the auction specified and store it in the master JSON"""
        page = 0
        run_loop = True
        while run_loop:
            try:
                payload = json.dumps({
                        "requests": [
                            {
                                "indexName": "wp_posts_lot_feature_sort_asc",
                                "params": f"facetFilters=%5B%5B%22taxonomies.auction_tax.name%3A{parse.quote(auction_name, encoding='utf-8', safe=':/')}%22%5D%5D",
                                "facets": [
                                    "taxonomies.sale_result.name",
                                    "taxonomies.auction_tax.name",
                                    "taxonomies.lot_type.name",
                                    "taxonomies.collection_tax.name",
                                    "taxonomies.lot_year.name",
                                    "taxonomies.make.name",
                                    "taxonomies.model.name",
                                    "taxonomies.body_type.name",
                                    "color_meta",
                                    "interior_meta",
                                    "engine_configuration_meta",
                                    "transmission_type_meta",
                                    "taxonomies.run_date.timestamp"
                                ],
                                "filters": "",
                                "highlightPostTag": "__/ais-highlight__",
                                "highlightPreTag": "__ais-highlight__",
                                "hitsPerPage": 96,
                                "maxValuesPerFacet": 50,
                                "page": 0,
                                "query": "",
                                "tagFilters": ""
                            },
                            {
                                "indexName": "wp_posts_lot_feature_sort_asc",
                                "params": "analytics=false&clickAnalytics=false&facets=taxonomies.auction"
                                        "_tax.name&filters=&highlightPostTag=__%2Fais-highlight__&highlightPreTag="
                                        "__ais-highlight__&hitsPerPage=0&maxValuesPerFacet=50&page=0&query="
                            }
                        ]
                    })

                response = self.session.post('https://u6cfcq7v52-1.algolianet.com/1/indexes/*/queries?x-alg'
                                        'olia-agent=Algolia%20for%20JavaScript%20(4.17.0)%3B%20Browser'
                                        '%20(lite)%3B%20instantsearch.js%20(4.55.0)%3B%20react%20(18.2'
                                        '.0)%3B%20react-instantsearch%20(6.38.1)%3B%20react-instantsea'
                                        'rch-hooks%20(6.38.1)%3B%20JS%20Helper%20(3.12.0)&x-algolia-ap'
                                        'i-key=0291c46cde807bcb428a021a96138fcb&x-algolia-application-'
                                        'id=U6CFCQ7V52', headers=auction_data_headers,
                                        data=payload,
                                        timeout=10)
            except Exception:
                print(Exception)
                import traceback
                traceback.print_exc()
                break


            master_data = response.json()['results'][0]['hits']

            if master_data:
                for data in master_data:
                    try:

                        item_url = data.get('permalink', "")
                        if item_url:
                            vin = self.get_vin(item_url)

                        try:
                            vehicle_type = data['post_type_label'] if 'post_type_label' in data else ""
                        except (TypeError, IndexError):
                            vehicle_type = ""

                        try:
                            item = data['post_title'] if 'post_title' in data else ""
                        except (TypeError, IndexError):
                            item = ""

                        try:
                            sale_date = (datetime.strptime(data['post_date_formatted'], '%B %d, %Y')
                                         if 'post_date_formatted' in data else "")
                        except (TypeError, IndexError):
                            sale_date = ""

                        try:
                            sale_time = (datetime.fromtimestamp(int(data['post_date'])).strftime('%H:%M:%S')
                                if 'post_date' in data else "")
                        except (TypeError, IndexError):
                            sale_time = ""

                        try:
                            day_of_week = (datetime.strptime(data['post_date_formatted'], '%B %d, %Y')
                                           .strftime('%A') if 'post_date_formatted' in data else "")
                        except (TypeError, IndexError):
                            day_of_week = ""

                        try:
                            color = data['color_meta'] if 'color_meta' in data else ""
                        except (TypeError, IndexError):
                            color = ""

                        try:
                            body_style = (data['taxonomies']['body_type'][0]['name']
                                            if 'body_type' in data['taxonomies'] else "")
                        except (TypeError, IndexError):
                            body_style =""

                        try:
                            engine = (data['engine_configuration_meta']
                                if 'engine_configuration_meta' in data else "")
                        except (TypeError, IndexError):
                            engine = ""

                        try:
                            lot_number = data['lot_number_meta'] if 'lot_number_meta' in data else ""
                        except (TypeError, IndexError):
                            lot_number = ""

                        try:
                            year = (data['taxonomies']['lot_year'][0]['name']
                                if 'lot_year' in data['taxonomies'] else "")
                        except (TypeError, IndexError):
                            year = ""

                        try:
                            est_retail_value = (data['high_estimate_meta'] if 'high_estimate_meta'
                                                in data else "")
                        except (TypeError, IndexError):
                            est_retail_value = ""

                        try:
                            transmission = (data['transmission_type_meta'] if 'transmission_type_meta'
                                            in data else "")
                        except (TypeError, IndexError):
                            transmission = ""

                        try:
                            sale_status = data['status_ranking'] if 'status_ranking' in data else ""
                        except (TypeError, IndexError):
                            sale_status = ""
                        yard_number = ""
                        yard_name = ""
                        time_zone = ""
                        try:
                            if 'make' in data['taxonomies'] and data['taxonomies']['make']:
                                 make = (data[
                                    'taxonomies']['make'][0]['name'])
                        except (TypeError, IndexError):
                            make = ""

                        model_group = ""

                        try:
                            if 'model' in data['taxonomies'] and data['taxonomies']['model']:
                                model_detail = (data[
                                    'taxonomies']['model'][0]['name'])
                        except (TypeError, IndexError):
                            model_detail = ""

                        try:
                            vin = vin if vin is not None else ""
                        except (TypeError, IndexError):
                            vin = ""
                        currency_code = "$"

                        try:
                            image_url = [image['url'] for image in data.get('images_meta', [])] if data.get('images_meta') else ""
                            image_urls = ",".join(image_url)
                        except (TypeError, IndexError):
                            image_urls = ""

                        damage_description = secondary_damage = sale_title_state =\
                        sale_title_type = has_keys = lot_cond_code = vin =\
                        odometer = odometer_brand = repair_cost = drive = fuel_type = \
                        cylinders = runs_drives = high_bid_non_vix_sealed_vix = \
                        special_note = location_city = location_state = location_zip5 = \
                             location_zip4 = location_country = image_thumbnail = create_date_time = \
                        grid_row = make_an_offer_eligible = buy_it_now_price = trim = \
                        last_updated_time = rentals = copart_select = source = ""

                        data = [yard_number, yard_name, sale_date, day_of_week, sale_time, time_zone, item, lot_number,
                        vehicle_type, year, make, model_detail, model_group, body_style, color, damage_description,
                        secondary_damage, sale_title_state, sale_title_type, has_keys, lot_cond_code, vin, odometer,
                        odometer_brand, est_retail_value, repair_cost, engine, drive, transmission,
                        fuel_type, cylinders, runs_drives, sale_status, high_bid_non_vix_sealed_vix, special_note,
                        location_city, location_state, location_zip5, location_zip4, location_country, currency_code,
                        image_thumbnail, create_date_time, grid_row, make_an_offer_eligible, buy_it_now_price, image_urls, trim,
                        last_updated_time, rentals, copart_select, source]

                        with open(f"{folder_name}/meccum_data.csv", "a", newline="", encoding="utf-8") as file:
                            writer = csv.writer(file)
                            writer.writerow(data)
                    except Exception as e:
                        print(e)
            else:
                break
            print(f"Page scraped till: {page}")
            page += 1

    def get_vin(self, item_url):
        item_page = self.session.get(f"https://www.mecum.com{item_url}",
                                                     headers=auction_data_headers)
        soup = bs(item_page.text, "lxml")
        try:
            vin = soup.find("div", class_="LotHeader_odometerSerial___fuHb").text.split(
                            "VIN / Serial")[-1].strip()
        except:
            vin = ""
        return vin

    @execution_time
    def scrap_all_auctions_data(self):
        """Scraps all the data from the website from different auctions and
         generated the CSV of the data"""
        auction_names = self.get_auction_names()
        with ThreadPoolExecutor() as executor:
            executor.map(self.get_auction_data, auction_names[:4])

if __name__ == "__main__":
    mecum_obj = MecumAuctions()
    mecum_obj.scrap_all_auctions_data()