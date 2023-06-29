"""
These modules are used to scrape the cars information from a website and saves it to a CSV file.

"""
# Install httpx and selectolax
import os
from typing import List
from urllib.parse import urljoin
import time
import datetime
from dataclasses import dataclass
import httpx
from httpx import ReadTimeout
from selectolax.parser import HTMLParser
#from rich import print
import pandas as pd
from bs4 import BeautifulSoup

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

cwd = os.path.abspath(os.getcwd())
folder_name = os.path.join(cwd, 'Output_folder',
                    datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S'))
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

@dataclass
class Product:
    """
    Represents a product:
    Attributes:
    item_value (str): The value of the item.
    specs (List[dict]): The specifications of the product, stored as a list of dictionaries.
    """
    item_value: str
    specs: List[dict]
@dataclass
class Response:
    """
    Represents a response:
    Attributes:
    body_html (str): The HTML body of the response.
    next_page (dict): The information about the next page, stored as a dictionary.

    """
    body_html: str  #HTMLParser
    next_page: dict

def get_page(client, url, retry=5, delay=30):

    """Fetches the HTML page from the specified URL and
    it uses retry option if the server doesn't support"""

    headers = {
        'authority': 'sca.auction',
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.'
        '36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'),
        }
    try:
        resp = client.get(url, headers=headers, timeout=60) # Set an appropriate timeout value
        html = HTMLParser(resp.text)
        next_page_element = html.css_first("a.pagination-v2__text.pagination-v2__text--next")
        if next_page_element is not None:
            next_page = {"href": next_page_element.attributes.get("href")}
        else:
            next_page = {"href": False}
        return Response(body_html=html, next_page=next_page)
    except ReadTimeout:
        if retry > 0:
            print("Timeout occurred. Retrying...")
            time.sleep(delay)  # Add a delay between retries if needed
            return get_page(client, url, retry=retry-1, delay=delay*2) # Exponential back-off
        #else:
        print("All retries exhausted. Retrying from the beginning...")
        time.sleep(delay)
        return get_page(client, url, retry=5, delay=30)  # Retry from the beginning

def extract_text(html, selector, index):

    """This function is used to extract text from html document based on
    css selector and index and it gives none if index is out of range"""

    try:
        return html.css(selector)[index].text(strip=True)
    except IndexError:
        return "None"


def parse_detail(html, product_url):

    """This function is responsible for scraping the product
    details from each product url and store that in an variable"""

    specs = [] # Initialize an empty list outside the loop
    print(product_url)
    spec_elements = html.css("div.lot-v2__panel-col.lot-v2__panel-col--third "
                             "section#lotVahicleInfo div.panel-info-v2__list")
    for spec_element in spec_elements:
        soup = BeautifulSoup(spec_element.html, 'html.parser')

        try:
            panel_div = soup.find('div', class_='panel-info-v2__list')
            vin_button = panel_div.find('button',
                                class_='panel-info-v2__vin').find_next_sibling('a')
            vin = vin_button['href']
            vin_value = vin.split('checkout/')[1].split('?')[0].strip().upper()
        except (AttributeError, TypeError):
            vin_value = "NA"
        try:
            odometer_value = soup.find('div', class_='panel-info-v2__desc',
                                       text=True).text.strip()
        except (AttributeError, TypeError):
            odometer_value = "NA"
    sales_info = []
    spec_elements2 = html.css("div.lot-v2__panel-col section.lot-v2__panel.lot-v2__panel"
                              "--desctop.panel-info-v2 div.panel-info-v2__list")
    for spec_element2 in spec_elements2:
        #print(spec_element2.html)
        soup2 = BeautifulSoup(spec_element2.html, 'html.parser')

        try:
            sale_date_value = soup2.find('div', class_="panel-info-v2__term",
                            text='Sale Date').find_next_sibling().text.strip().split(',')[0]
            sales_info.append(sale_date_value)
            #print(sale_date_value)
        except (AttributeError, TypeError):
            sale_date_value = "NA"
            sales_info.append(sale_date_value)
        try:
            sale_time_value = soup2.find('div', class_="panel-info-v2__term",
                            text='Sale Date').find_next_sibling().text.strip().split(', ')[1]
            sales_info.append(sale_time_value)
            #print(sale_time_value)
        except (AttributeError, TypeError):
            sale_time_value = "NA"
            sales_info.append(sale_time_value)
        try:
            sale_title_state_values = soup2.find('div', class_="panel-info-v2__term",
                                    text='Sale Location').find_next_sibling().text.strip()
            sale_title_state_value = sale_title_state_values.split('\n')[0].strip()
            sales_info.append(sale_title_state_value)
            #print(sale_title_state_value)
        except (AttributeError, TypeError):
            sale_title_state_value = "NA"
            sales_info.append(sale_title_state_value)
        try:
            last_updated_time_value = soup2.find('div', class_="panel-info-v2__term",
                                    text='Last Updated').find_next_sibling().text.strip()
            sales_info.append(last_updated_time_value)
            #print(last_updated_time_value)
        except (AttributeError, TypeError):
            last_updated_time_value = "NA"
            sales_info.append(last_updated_time_value)
        sale_title_type = ""
        secondary_damage_value = ""
        repair_cost_value = ""
        drive_value = ""
        odometer_brand_value = ""
        est_retail_value = ""
        has_keys = ""
        lot_cond_code = ""
        time_zone_value = ""
        source_value = ""
        yard_number_value = ""
        yard_name_value = ""
        day_of_week_value = ""
        lot_number_value = ""
        model_group_value = ""
        damage_description_value = ""
        runs_drives_value = ""
        sale_status_value = ""
        high_bid_non_vix_sealed_vix_value = ""
        special_note_value = ""
        location_city_value = ""
        location_state_value = ""
        location_zip5_value = ""
        location_zip4_value = ""
        location_country_value = ""
        currency_code_value = ""
        create_date_time_value = ""
        grid_row_value = ""
        make_an_offer_eligible_value = ""
        buy_it_now_price_value = ""
        trim_value = ""
        rentals_value = ""
        copart_select_value = ""
    spec_elements1 = html.css("div.lot-v2__panel-col.lot-v2__panel-col--third "
                              "section#lotVehicleDesc div.panel-info-v2__list")
    for spec_element1 in spec_elements1:
        soup1 = BeautifulSoup(spec_element1.html, 'html.parser')

        try:
            vehicle_type_value = soup1.find('div', class_="panel-info-v2__term",
                                text='Vehicle Type').find_next_sibling().text.strip()
        except (AttributeError, TypeError):
            vehicle_type_value = "NA"
        try:
            year_value = soup1.find('div', class_="panel-info-v2__term",
                        text='Year').find_next_sibling().text.strip()
        except (AttributeError, TypeError):
            year_value = "NA"
        try:
            make_value = soup1.find('div', class_="panel-info-v2__term",
                        text='Make').find_next_sibling().text.strip()
        except (AttributeError, TypeError):
            make_value = "NA"

        try:
            model_detail_value = soup1.find('div', class_="panel-info-v2__term",
                                text='Model').find_next_sibling().text.strip()
        except (AttributeError, TypeError):
            model_detail_value = "NA"
        try:
            body_style_value = soup1.find('div', class_="panel-info-v2__term",
                                text='Body Style').find_next_sibling().text.strip()
        except (AttributeError, TypeError):
            body_style_value = "NA"
        try:
            color_value = soup1.find('div', class_="panel-info-v2__term",
                        text='Exterior Color').find_next_sibling().text.strip()
        except (AttributeError, TypeError):
            color_value = "NA"

        try:
            engine_value = soup1.find('div', class_="panel-info-v2__term",
                        text='Engine').find_next_sibling().text.strip()
        except (AttributeError, TypeError):
            engine_value = "NA"
        try:
            transmission_value = soup1.find('div', class_="panel-info-v2__term",
                                text='Transmission').find_next_sibling().text.strip()
        except (AttributeError, TypeError):
            transmission_value = "NA"

        try:
            fuel_type_value = soup1.find('div', class_="panel-info-v2__term",
                            text='Fuel Type').find_next_sibling().text.strip()
        except (AttributeError, TypeError):
            fuel_type_value = "NA"
        try:
            cylinders_value = soup1.find('div', class_="panel-info-v2__term",
                            text='Cylinders').find_next_sibling().text.strip()
        except (AttributeError, TypeError):
            cylinders_value = "NA"
    html_str = html.html if isinstance(html.html, str) else html.html.decode()
    soup3 = BeautifulSoup(html_str, 'html.parser')
    try:
        image_thumbnail_value = soup3.find('div', class_="lot-v2__panel-col"
                                ).find('picture', class_="lot_main_image").img.get('src')
    except (AttributeError, TypeError):
        image_thumbnail_value = "NA"
    try:
        image_urls_value = soup3.find('div', class_="lot-v2__slider-thumbs")
        image_urls_value1 = image_urls_value.find_all('picture')
        image_url_value = []
        for picture in image_urls_value1:
            img_tag = picture.find('img')
            if img_tag is not None and 'src' in img_tag.attrs:
                image_url = img_tag['src']
                image_url_value.append(image_url)
    except (AttributeError, TypeError):
        image_url_value = "NA"
    # Create a dictionary for each specification and add it to the list
    spec_dict = {"value1": vin_value, "value2": odometer_value, "value3":vehicle_type_value,
                 "value4": year_value, "value5" : make_value,"value6": model_detail_value,
                 "value7": body_style_value, "value8": color_value, "value9": engine_value,
                 "value10": transmission_value,"value11": fuel_type_value,
                 "value12": cylinders_value, "value13": sales_info[0], "value14":sales_info[1],
                 "value15": sales_info[2], "value16":sales_info[3], "value17": image_thumbnail_value,
                 "value18":image_url_value,"value19": sale_title_type, "value20":secondary_damage_value,
                 "value21": repair_cost_value, "value22": drive_value,"value23": odometer_brand_value,
                 "value24": est_retail_value, "value25":has_keys, "value26": lot_cond_code,
                 "value27": time_zone_value, "value28":source_value, "value29":yard_number_value,
                 "value30":yard_name_value,"value31":day_of_week_value, "value32":lot_number_value,
                 "value33":model_group_value, "value34":damage_description_value,
                 "value35":runs_drives_value, "value36":sale_status_value,
                 "value37":high_bid_non_vix_sealed_vix_value, "value38":special_note_value,
                 "value39":location_city_value, "value40":location_state_value, "value41":location_zip5_value,
                 "value42":location_zip4_value,"value43":location_country_value, "value44":currency_code_value,
                 "value45":create_date_time_value, "value46":grid_row_value,"value47":make_an_offer_eligible_value,
                 "value48":buy_it_now_price_value, "value49":trim_value, "value50":rentals_value,
                 "value51":copart_select_value,
                 }
    specs.append(spec_dict)
    new_product = Product(
        item_value = extract_text(html, "h1.title-v2.lot-v2__title", 0),
        #url=url,
        specs=specs
        )
    return new_product
    #print(new_product)
def detail_page_loop(client, page):

    "This function is responsible for iterating over a list of product links and retrive detailed info of each product"

    products = [] # List to store products from all pages
    base_url = "https://sca.auction"
    product_links = parse_links(page.body_html)
    url_count = 0  # Initialize URL count
    for link in product_links:
        #detail_page = get_page(client, urljoin(base_url, link))
        product_url = urljoin(base_url, link)
        detail_page = get_page(client, product_url)
        if detail_page is not None:
            product = parse_detail(detail_page.body_html, product_url)
            if product is not None:
                products.append(product) # Add the product to the list
        # Add a time gap of 2 seconds between each iteration
        time.sleep(3)  # Add a time gap of 3 seconds between each product detail
        url_count += 1  # Increment URL count
        print(f"Processed URL {url_count}/{len(product_links)}")  # Print the progress
    #write_to_csv(products) # if we write here then it only prints the each page values and it doesn't store all the products
    return products

def write_to_csv(products):

    "This function is used to create csv file using pandas and store all the product details in it"

    data = []
    for product in products:
        for spec in product.specs:
            row = {
                "Item": product.item_value,
                "VIN": spec["value1"],
                "Odometer": spec["value2"],
                "Vehicle Type": spec["value3"],
                "Year": spec["value4"],
                "Make": spec["value5"],
                "Model Detail": spec["value6"],
                "Body Style": spec["value7"],
                "Color": spec["value8"],
                "Engine": spec["value9"],
                "Transmission": spec["value10"],
                "Fuel Type": spec["value11"],
                "Cylinders": spec["value12"],
                "Sale Date": spec.get("value13"),
                "Sale Time": spec.get('value14'),
                "Sale Title State": spec.get('value15'),
                "Last Updated Time": spec.get('value16'),
                "Image Thumbnail":spec['value17'],
                "Image URLS": spec['value18'],
                "Sale Title": spec['value19'],
                "Secondary Damage":spec['value20'],
                "Repair Cost": spec['value21'],
                "Drive":spec['value22'],
                "Odometer Brand":spec['value23'],
                "Est Retail Value":spec['value24'],
                "Has Keys":spec['value25'],
                "Lot Cond Code":spec['value26'],
                "Time Zone":spec['value27'],
                "Source":spec['value28'],
                "Yard Number": spec['value29'],
                "Yard Name": spec['value30'],
                "Day of Week":spec['value31'],
                "Lot Number":spec['value32'],
                "Model Group":spec['value33'],
                "Damage Description":spec['value34'],
                "Runs Drives":spec['value35'],
                "Sale Status":spec['value36'],
                "High_bid_non_vix_sealed_vix":spec['value37'],
                "Special Note":spec['value38'],
                "Location City":spec['value39'],
                "Location State":spec['value40'],
                "Location Zip5":spec['value41'],
                "Location Zip4":spec['value42'],
                "Location Country":spec['value43'],
                "Currency Code":spec['value44'],
                "Create Date Time":spec['value45'],
                "Grid Row":spec['value46'],
                "Make an offer eligible":spec['value47'],
                "Buy it now price":spec['value48'],
                "Trim":spec['value49'],
                "Rentals":spec['value50'],
                "Copart Select":spec['value51']


                }
            data.append(row)
    data_frame = pd.DataFrame(data)
    # Get current date and time
    filename = f"{folder_name}/sca_auction_csv.csv"
    data_frame.to_csv(filename, index=False)
    #data_frame.to_csv("sca_auction_output11.csv", index=False)

def parse_links(html):

    "This function takes html document as input and parse it to extract the product links that match css selector"

    links = html.css("ul.search-v2__result-lots li.result-lots__item article.result-lots__wrap a.result-lots__slide")
    return {link.attributes["href"] for link in links} # here we are using set to delete duplicate elements


def pagination_loop(client, max_page=35):

    """
    This function is used to pull all the page urls from the website.

    Args:
    client (httpx.Client): HTTP client for making requests
    max_page (int, optional): Maximum number of pages to fetch

    """
    today = datetime.datetime.today()
    formatted_date = today.strftime('%m-%d-%Y')

    url = f"https://sca.auction/en/search/sale-date-{formatted_date}-to-{formatted_date}"
    all_products = []  # List to store products from all pages
    page_count = 0
    while True:
        page = get_page(client, url) # Fetch the initial page
        prod = detail_page_loop(client, page) # Parse product details
        all_products.extend(prod)  # Add the products from the current page to the combined list
        page_count += 1
        if page.next_page["href"] is False or page_count>= max_page:
            client.close()
            break
        #else:
        url = urljoin(url, page.next_page["href"])
        print(url)
    write_to_csv(all_products)  # Write all the products to the CSV file

def main():
    "This is the entry point of the program, It sets up an HTTP client using httpx and then calls pagination loop"
    client = httpx.Client()
    pagination_loop(client, max_page=35)

if __name__ == "__main__":
    main()
    print("Scrapped the urls")
