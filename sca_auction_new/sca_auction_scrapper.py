import os
import sys
import requests
import csv
from datetime import datetime
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor

from constants import (headers, params,vehicle_headers,
                       cookies, folder_name)

class ScaAuctionScrapper:
    """
    This will get all the data of current date bid
    """
    def __init__(self):
        """
        Initializing function
        """

        self.session = requests.Session()
        self.all_links = set()
        self.max_page = 0
        self.user_agent = UserAgent()


    def make_first_request(self):
        """
        Making first request which helps in getting the
        total pages
        """
        response = self.session.get('https://sca.auction/en/vehicle/search/indexAjax',
                        params=params, headers=headers)
        self.soup = bs(response.content, "lxml")
        self.soup.prettify()
        # with open("try.txt", "w", encoding="utf-8") as file_:
        #     file_.write(str(self.soup))

        pages = self.get_total_pages()
        if pages:
            all_links_tags = self.soup.find_all("a" ,class_="result-lots__slide")

            for links in all_links_tags:
                self.all_links.add(links['href'])

    def get_total_pages(self):
        """
        This is to get the total number of pages
        """
        try:
            all_pages = self.soup.find_all("a", class_="pagination-v2__text")
            # print(all_pages)
            for page_tags in all_pages:
                if int(page_tags['data-page']) > self.max_page:
                    self.max_page = int(page_tags['data-page'])
                    print(f"The total pages are: {self.max_page}")
                else:
                    pass
            return self.max_page
        except AttributeError:
            print("No data available for today's date")
            sys.exit()


    def get_all_vehicle_links(self, current_page):
        """
        This is to get link of all today's bid vehicles
        """
        # cookies.update(cookies2)
        try:
            print(f"scrapping page {current_page}")
            params['page'] = current_page
            headers['user-agent'] = self.user_agent.random

            response = requests.get('https://sca.auction/en/vehicle/search/indexAjax',
                            params=params, cookies=cookies, headers=headers)
            soup = bs(response.content, "lxml")

            all_links_tags = soup.find_all("a" ,class_="result-lots__slide")
            for links in all_links_tags:
                self.all_links.add(links['href'])
        except Exception as e:
            print(f"This is the exception here: {e}")

    def get_vehicle_details(self, vehicle_link):
        """
        To get the entire detail of the bid vehicle
        """
        # cookies.update(cookies2)
        overall_data =  {}
        vehicle_headers['user-agent'] = self.user_agent.random
        vehicle_response = requests.get(f'https://sca.auction{vehicle_link}',
                                        cookies=cookies, headers=vehicle_headers)

        vehicle_soup = bs(vehicle_response.content, "lxml")

        # get all the details

        vehicle_description_section = vehicle_soup.find("section", id="lotVehicleDesc")
        all_desc_list = vehicle_description_section.find("div", class_="panel-info-v2__list")

        vehicle_information = self.get_vehicle_description(all_desc_list)

        vehicle_extra_info_section = vehicle_soup.find("section", id="lotVahicleInfo")
        all_extra_desc_list = vehicle_extra_info_section.find("div", class_="panel-info-v2__list")

        bid_info =  vehicle_soup.find("section", id="lotBidInfo")


        vehicle_extra_information = self.get_extra_information(all_extra_desc_list)

        sales_information = self.get_sales_information(vehicle_soup)

        try:
            bid_information = self.get_bid_details(bid_info)
        except Exception as e:
            print(e)

        try:
            images_data = self.get_images(vehicle_soup)
        except Exception as e:
            print(e, "in the images file")

        # empty data
        empty_data = {'yard_name':"", "yard_number":"", "timezone":"EDT", "lot_number":"",
                      "sale_title_type":"", "lot_cond_code":"","odometer_brand":"",
                      "est_retail_value":"","repair_cost":"", "drive":"", "runs_drives":"",
                      "sale_status":"Available","high_bid_non_vix_sealed_vix":"","special_note":"",
                      'location_city':"", 'location_state':"", 'location_zip5':"", 'location_zip4':"",
                      "location_country":"USA","currency_code":"$", "create_date_time":"",
                      "grid_row":"","make_an_offer_eligible":"", "trim":"", "source":"", "copart_select":"",
                      "rentals":""}

        #     Timestamp
        empty_data['buy_it_now_price'] = bid_information
        overall_data.update(sales_information)
        overall_data.update(vehicle_information)
        overall_data.update(vehicle_extra_information)
        overall_data.update(empty_data)
        overall_data.update(images_data)

        csv_file = "combined_data.csv"
        fieldnames = overall_data.keys()

        try:
            with open(f"{folder_name}/csv_file", "a", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                is_empty = os.stat(csv_file).st_size == 0
                if is_empty:
                    writer.writeheader()
                writer.writerow(overall_data)
        except Exception as e:
            print(e)

    def get_images(self, main_soup):
        """
        This is to get all the images
        """
        images_dict = {"image_thumbnail":"", "image_url":""}

        picture = main_soup.find("picture", class_="lot_main_image")
        main_img = picture.find("img")
        if main_img:
            images_dict["image_thumbnail"] = main_img["src"]

        try:
            image_urls_value = main_soup.find("div", class_="carousel-v2__item lot-v2__slide")
            image_urls_value1 = image_urls_value.find_all("picture")
            image_url_value = []
            for picture in image_urls_value1:
                img_tag = picture.find("img")
                if img_tag is not None and "src" in img_tag.attrs:
                    image_url = img_tag["src"]
                    image_url_value.append(image_url)
        except (AttributeError, TypeError):
            image_url_value = " "

        images_dict["image_url"]: image_url_value
        return images_dict


    def get_sales_information(self, main_soup):
        """
        This will get the data related to sales
        """
        sales_info = {
            "item":"", "sale_title_state": "", "sale_date": "", "sale_time": "", "day_of_week": "",
             "last_updated_time":"",
        }
        # panel-info-v2__desc panel-info-v2__desc--price
        item = main_soup.find("h1", id="lotLabel").text.strip()
        sales_info["item"] = item

        sales_table = main_soup.select("section.lot-v2__panel.lot-v2__panel--desctop.panel-info-v2")
        sales_div = sales_table[0].find("div", class_="panel-info-v2__list")
        all_items = sales_div.find_all("div", class_="panel-info-v2__item")
        for info_ in all_items:
            if "Sale Location" in info_.text.strip():
                sales_info["sale_title_state"] = info_.find("button").text
            elif "Sale Date" in info_.text.strip():
                datetimeinfo = info_.find("div", class_="panel-info-v2__desc").text.strip().split("(EDT)")[0].strip()
                # Define the format of the timestamp
                timestamp_format = "%a %b %d, %I:%M%p"
                # Parse the timestamp string into a datetime object
                dt = datetime.strptime(datetimeinfo, timestamp_format)

                # Extract the day, time, and date from the datetime object
                day = dt.strftime("%A")
                time_ = dt.strftime("%I:%M %p")
                date = dt.strftime("%B %d")
                sales_info["day_of_week"] = day
                sales_info["sale_date"] = date
                sales_info["sale_time"] = time_
            elif "Last Updated" in info_.text.strip():
                sales_info["last_updated_time"] = info_.find("div", class_="panel-info-v2__desc").text.strip()
        return sales_info


    def get_vehicle_description(self, description_soup):
        """
        This will get the vehicle description
        """
        all_desc_list = description_soup.find_all("div", class_="panel-info-v2__item")

        vehicle_info = {
            "type": "", "year": "", "make": "", "model_detail": "",
            "model_group": "", "body_style": "", "color": "", "engine": "",
            "transmission": "", "fuel_type": "", "cylinders": ""
        }

        attribute_mappings = {
            "Vehicle Type": "type", "Year": "year", "Make": "make",
            "Model": "model_group", "Body Style": "body_style",
            "Exterior Color": "color", "Engine": "engine",
            "Transmission": "transmission", "Fuel Type": "fuel_type",
            "Cylinders": "cylinders"
        }

        for list_ in all_desc_list:
            heading = list_.find("div", class_="panel-info-v2__term")
            attribute = attribute_mappings.get(heading.text.strip().replace(" ",""))
            if attribute:
                value = heading.find_next_sibling("div").text
                vehicle_info[attribute] = value

        return vehicle_info


    def get_extra_information(self, extra_description_soup):
        """
        This will get the vehicle description
        """
        all_desc_list = extra_description_soup.find_all("div", class_="panel-info-v2__item")

        vehicle_extra_info = {
            "vin":"", "has_keys": "", "odometer": "", "secondary_damage": "",
            "damage_description": "",
        }

        for list_ in all_desc_list:
            heading = list_.text.strip()
            if "VIN" in heading:
                a_tag = list_.find("a")
                vehicle_extra_info["vin"] = a_tag['href'].split("checkout/")[1].split("?")[0].strip().upper()
            if "Odometer" in heading:
                vehicle_extra_info["odometer"] = list_.find("div",
                                class_="panel-info-v2__desc").text.strip()
            elif "Secondary Damage" in heading:
                vehicle_extra_info["secondary_damage"] = list_.find("div",
                                class_="panel-info-v2__desc").text.strip()
            elif "Key" in heading:
                vehicle_extra_info["has_keys"] = list_.find("div",
                                class_="panel-info-v2__desc").text.strip()

        return vehicle_extra_info


    def get_bid_details(self, bid_soup):
        """
        This is to get the bid info
        """
        current_bid = ""
        current_bid = bid_soup.find("div", class_="panel-info-v2__desc panel-info-v2__desc--price").text
        print(f"current_bid:{current_bid}")
        return current_bid


if __name__ == "__main__":
    sca_scrapper = ScaAuctionScrapper()
    sca_scrapper.make_first_request()

    with ThreadPoolExecutor() as executor:
        executor.map(sca_scrapper.get_all_vehicle_links,
                     range(2, sca_scrapper.max_page+1))

    print(len(sca_scrapper.all_links))
    with ThreadPoolExecutor() as executor:
        executor.map(sca_scrapper.get_vehicle_details,
                     sca_scrapper.all_links)
