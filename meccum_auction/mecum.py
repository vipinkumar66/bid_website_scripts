""""Module to extract the bids' data from Mecum Website"""
# Importing Required Libraries
import time
from urllib import parse
from functools import wraps
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from config import folder_name, auction_url, auction_data_headers


class MecumAuctions:
    """Extracts the data of Bids from Mecum Bids Website"""
    def __init__(self):
        self.session = requests.session()
        self.master_json = {"yard_number": [], "yard_name": [], "sale_date": [],
                            "day_of_week": [], "sale_time": [], "time_zone": [], "item": [],
                            "lot_number": [], "vehicle_type": [], "year": [], "make": [],
                            "model_group": [], "model_detail": [], "body_style": [], "color": [],
                            "damage_description": [], "secondary_damage": [],
                            "sale_title_state": [], "sale_title_type": [], "has_keys": [],
                            "lot_cond_code": [], "vin": [], "odometer": [], "odometer_brand": [],
                            "est_retail_value": [], "repair_cost": [], "engine": [], "drive": [],
                            "transmission": [], "fuel_type": [], "cylinders": [], "runs_drives": [],
                            "sale_status": [], "high_bid_non_vix_sealed_vix": [],
                            "special_note": [], "location_city": [], "location_state": [],
                            "location_zip5": [], "location_zip4": [], "location_country": [],
                            "currency_code": [], "image_thumbnail": [], "create_date_time": [],
                            "grid_row": [], "make_an_offer_eligible": [], "buy_it_now_price": [],
                            "image_url": [], "trim": [], "last_updated_time": [], "rentals": [],
                            "copart_select": [], "source": []}

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
        for auc in auctions_data:
            auc_title = auc['node']['title']
            auc_start_date = datetime.strptime(auc['node']['auctionFields']['auctionStartDate'],
                                               '%B %d, %Y') + timedelta(hours=5.5)
            auc_end_date = datetime.strptime(auc['node']['auctionFields']['auctionEndDate'],
                                             '%B %d, %Y') + timedelta(hours=5.5)
            auc_string = f"{auc_title}|{int(time.mktime(auc_start_date.timetuple()))}|" \
                         f"{int(time.mktime(auc_end_date.timetuple()))}"
            auctions_names.append(auc_string)
        return auctions_names

    def get_auction_data(self, auction_name):
        """Extract the data of the auction specified and store it in the master JSON"""
        page = 0
        run_loop = True
        while run_loop:

            data = '{"requests":[{"indexName":"wp_posts_lot_feature_sort_asc","params":"facetFil' \
                   'ters=%5B%5B%22taxonomies.auction_tax.name%3A' + parse.quote(auction_name) + \
                   '%22%5D%5D&facets=%5B%22taxonomies.sale_result.name%22%2C%22taxonomies.auction' \
                   '_tax.name%22%2C%22taxonomies.lot_type.name%22%2C%22taxonomies.collection_tax.' \
                   'name%22%2C%22taxonomies.lot_year.name%22%2C%22taxonomies.make.name%22%2C%22ta' \
                   'xonomies.model.name%22%2C%22taxonomies.body_type.name%22%2C%22color_meta%22%2' \
                   'C%22interior_meta%22%2C%22engine_configuration_meta%22%2C%22transmission_type' \
                   '_meta%22%2C%22taxonomies.run_date.timestamp%22%5D&filters=&highlightPostTag=_' \
                   '_%2Fais-highlight__&highlightPreTag=__ais-highlight__&hitsPerPage=96&maxValue' \
                   'sPerFacet=50&page=' + str(page) + \
                   '&query=&tagFilters="},{"indexName":"wp_posts_lot_feature_sort_asc","params":"' \
                   'analytics=false&clickAnalytics=false&facets=taxonomies.auction_tax.name&filte' \
                   'rs=&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&h' \
                   'itsPerPage=0&maxValuesPerFacet=50&page=0&query="}]}'
            response = self.session.post('https://u6cfcq7v52-1.algolianet.com/1/indexes/*/queries?x-alg'
                                     'olia-agent=Algolia%20for%20JavaScript%20(4.17.0)%3B%20Browser'
                                     '%20(lite)%3B%20instantsearch.js%20(4.55.0)%3B%20react%20(18.2'
                                     '.0)%3B%20react-instantsearch%20(6.38.1)%3B%20react-instantsea'
                                     'rch-hooks%20(6.38.1)%3B%20JS%20Helper%20(3.12.0)&x-algolia-ap'
                                     'i-key=0291c46cde807bcb428a021a96138fcb&x-algolia-application-'
                                     'id=U6CFCQ7V52', headers=auction_data_headers, data=data, timeout=10)
            master_data = response.json()['results'][0]['hits']
            # with open("text.txt", "w", encoding="utf-8") as file_:
            #     file_.write(master_data)
            if master_data:
                for data in master_data:
                    try:

                        item_url = data.get('permalink', "")
                        if item_url:
                            vin = self.get_vin(item_url)

                        self.master_json["vehicle_type"].append(data['post_type_label']
                                                                if 'post_type_label' in data else "")
                        self.master_json["item"].append(data['post_title']
                                                        if 'post_title' in data else "")
                        self.master_json["sale_date"].append(datetime.strptime(
                            data['post_date_formatted'], '%B %d, %Y')
                                                            if 'post_date_formatted' in data else "")
                        self.master_json["sale_time"].append(
                            datetime.fromtimestamp(int(data['post_date'])).strftime('%H:%M:%S')
                            if 'post_date' in data else "")
                        self.master_json["day_of_week"].append(
                            datetime.strptime(data['post_date_formatted'], '%B %d, %Y').strftime('%A')
                            if 'post_date_formatted' in data else "")
                        self.master_json["color"].append(
                            data['color_meta'] if 'color_meta' in data else "")
                        self.master_json["body_style"].append(
                            data['taxonomies']['body_type'][0]['name']
                            if 'body_type' in data['taxonomies'] else "")
                        self.master_json["engine"].append(
                            data['engine_configuration_meta']
                            if 'engine_configuration_meta' in data else "")
                        self.master_json["lot_number"].append(
                            data['lot_number_meta'] if 'lot_number_meta' in data else "")
                        self.master_json["year"].append(
                            data['taxonomies']['lot_year'][0]['name']
                            if 'lot_year' in data['taxonomies'] else "")
                        self.master_json["est_retail_value"].append(
                            data['high_estimate_meta'] if 'high_estimate_meta' in data else "")
                        self.master_json["transmission"].append(
                            data['transmission_type_meta'] if 'transmission_type_meta' in data else "")
                        self.master_json["sale_status"].append(
                            data['status_ranking'] if 'status_ranking' in data else "")
                        self.master_json["yard_number"].append("")
                        self.master_json["yard_name"].append("")
                        self.master_json["time_zone"].append("")
                        if 'make' in data['taxonomies'] and data['taxonomies']['make']:
                            self.master_json["make"].append(data[
                                'taxonomies']['make'][0]['name'])
                        else:
                            self.master_json["make"].append("")

                        self.master_json["model_group"].append("")

                        if 'model' in data['taxonomies'] and data['taxonomies']['model']:
                            self.master_json["model_detail"].append(data[
                                'taxonomies']['model'][0]['name'])
                        else:
                            self.master_json["model_detail"].append("")

                        self.master_json["damage_description"].append("")
                        self.master_json["secondary_damage"].append("")
                        self.master_json["sale_title_state"].append("")
                        self.master_json["sale_title_type"].append("")
                        self.master_json["has_keys"].append("")
                        self.master_json["lot_cond_code"].append("")
                        self.master_json["vin"].append(vin if vin is not None else "")
                        self.master_json["odometer"].append("")
                        self.master_json["odometer_brand"].append("")
                        self.master_json["repair_cost"].append("")
                        self.master_json["drive"].append("")
                        self.master_json["fuel_type"].append("")
                        self.master_json["cylinders"].append("")
                        self.master_json["runs_drives"].append("")
                        self.master_json["high_bid_non_vix_sealed_vix"].append("")
                        self.master_json["special_note"].append("")
                        self.master_json["location_city"].append("")
                        self.master_json["location_state"].append("")
                        self.master_json["location_zip5"].append("")
                        self.master_json["location_zip4"].append("")
                        self.master_json["location_country"].append("")
                        self.master_json["currency_code"].append("")
                        self.master_json["image_thumbnail"].append("")
                        self.master_json["create_date_time"].append("")
                        self.master_json["grid_row"].append("")
                        self.master_json["make_an_offer_eligible"].append("")
                        self.master_json["buy_it_now_price"].append("")
                        image_urls = [image['url'] for image in data['images_meta']]
                        self.master_json["image_url"].append(",".join(image_urls))
                        self.master_json["trim"].append("")
                        self.master_json["last_updated_time"].append("")
                        self.master_json["rentals"].append("")
                        self.master_json["copart_select"].append("")
                        self.master_json["source"].append("")
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
        vin = soup.find("div", class_="LotHeader_odometerSerial___fuHb").text.split(
                            "VIN / Serial")[-1].strip()
        return vin

    @execution_time
    def scrap_all_auctions_data(self, output_file_name):
        """Scraps all the data from the website from different auctions and
         generated the CSV of the data"""
        auction_names = self.get_auction_names()
        print(f"Total auctions: {len(auction_names)}")
        with ThreadPoolExecutor() as executor:
            executor.map(self.get_auction_data, auction_names)
        for i in self.master_json:
            print(len(self.master_json[i]))
        dataframe = pd.DataFrame(self.master_json)
        dataframe.to_csv(f"{folder_name}/{output_file_name}", index=False)

if __name__ == "__main__":
    mecum_obj = MecumAuctions()
    mecum_obj.scrap_all_auctions_data(output_file_name="Mecum_Auctions_Data.csv")

