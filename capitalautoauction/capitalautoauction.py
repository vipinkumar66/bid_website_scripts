import requests
from constants import (headers, cookies,
                       csv_headers)
from bs4 import BeautifulSoup as bs
from concurrent.futures import ThreadPoolExecutor
import csv
import re

class CarsBids:

    def __init__(self) -> None:
        self.session = requests.Session()
        self.auction_links_list = []
        self.items_link = []
        self.data = {"VIN":"", "Stock#":"", "Year":"", "Make":"", "Model":"",
                "Type":"", "Drive":"", "Odo":"", "Engine":"", "Transmission":"",
                "Ext color":"",'yard_number':"", 'yard_name':"", 'Live Start':"",
                'day_of_week':"", 'Event':"", 'time_zone':"", 'item':"",'lot_number':"",
                'vehicle_type':"", 'year':"", 'make':"", 'model_group':"",
                'model_detail':"", 'body_style':"", 'color':"",'damage_description':"",
                'secondary_damage':"", 'sale_title_state':"", 'sale_title_type':"",
                'has_keys':"",'lot_cond_code':"", 'odometer_brand':"", 'est_retail_value':"",
                'repair_cost':"", 'fuel_type':"", 'cylinders':"", 'runs_drives':"",
                'sale_status':"",'high_bid_non_vix_sealed_vix':"",'special_note':"",
                'Location':"", 'location_state':"", 'location_zip5':"", 'location_zip4':"",
                'location_country':"", 'currency_code':"$", 'image_thumbnail':"",
                'create_date_time':"", 'grid_row':"",'make_an_offer_eligible':"",
                'Current Bid':"", 'image_url':"", 'trim':"", 'last_updated_time':"",
                'rentals':"",'copart_select':"", 'source':"", 'Timestamp':""}

    def get_auction_links(self) -> list:

        response = self.session.get(url='https://www.capitalautoauction.com/', cookies=cookies, headers=headers)
        soup = bs(response.content, "lxml")

        # GETTING LINKS FOR ALL THE CURRENT AND UPCOMING AUCTIONS
        all_auctions_links = soup.find_all("div", class_="auction-calendar__event-reference")

        for auctions in all_auctions_links:
            try:
                links = auctions.find("a")
                self.auction_links_list.append(links["href"])
            except TypeError:
                pass
        return self.auction_links_list

    def get_items_from_auctions(self, links):
        page = 1
        while True:
            try:
                auction_pages = f"{links}&page={page}"
                print(auction_pages)
                headers['referer'] = links
                response = self.session.get(auction_pages, headers=headers, cookies=cookies)
                soup = bs(response.content, "lxml")

                catalog_cards = soup.find("div", class_="catalog__cards")
                all_cards_data = catalog_cards.find_all("div", class_=("card", "catalog__card"))
                for cards in all_cards_data:
                    buttons = cards.select("div.card__buttons")[1]
                    a_tags = buttons.find_all("a")
                    self.get_items_data(a_tags[1]['href'])
                page+=1
            except Exception as e:
                break

    def get_items_data(self, items_links):
        print(items_links)
        response = self.session.get(f"{items_links}/", headers=headers, cookies=cookies)
        print(response.status_code)
        soup = bs(response.content, "lxml")

        vehicle_title = soup.find("h1", class_="vehicle__title").text.replace(" ","")
        self.data['item'] = re.sub(r"\s", " ", vehicle_title)

        # Vehicle data
        vehicle_data_details = soup.select("div.options.options--frame.vehicle__options")[0]
        try:
            for item in vehicle_data_details.find_all('li', class_='options__item'):
                heading = item.select('span.options__label')[0].get_text().strip()
                if heading.split(":")[0].strip() in csv_headers:
                    value = item.select('span.options__value')[0].get_text().strip().replace("\n","")
                    self.data[heading.split(":")[0].strip()] = value
                else:
                    pass

            # Auction Data
            auction_data_details = soup.find("div", id="bid_now")
            location_date_div = auction_data_details.find("div",class_=("options","vehicle__data-options"))
            # bids = soup.find_all("div", class_="vehicle__bid")
            # print(bids)
            # self.data['Current Bid'] = bids.text.split().strip(":")[1]

            for item in location_date_div.find_all('li', class_='options__item'):
                heading = item.select('span.options__label')[0].get_text().strip()
                if heading.split(":")[0].strip() in csv_headers:
                    if heading.split(":")[0].strip() == "Event":
                        print("here")
                        value_text = item.select('span.options__value')[0].get_text().strip()
                        value = " ".join(re.findall(r'\b\d{2}:\d{2} [ap]m\b',value_text))
                    value = item.select('span.options__value')[0].get_text().strip().replace("\n","")
                    self.data[heading.split(":")[0].strip()] = value
                else:
                    pass
            with open("data.csv", "a", newline="", encoding="utf_8") as csv_file:
                writer = csv.DictWriter(csv_file,fieldnames=csv_headers)
                writer.writerow(self.data)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    obj = CarsBids()
    with open("data.csv", "w", newline="", encoding="utf_8") as csv_file:
        writer = csv.DictWriter(csv_file,fieldnames=csv_headers)
        writer.writeheader()
    auction_list = obj.get_auction_links()
    with  ThreadPoolExecutor() as executor:
        executor.map(obj.get_items_from_auctions, auction_list)




