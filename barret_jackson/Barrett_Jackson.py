"""
Import Required Libraries
"""
import csv
import os
import re
import datetime
from concurrent.futures import ThreadPoolExecutor
from functools import wraps
import time
import requests
from retrying import retry
from bs4 import BeautifulSoup

class BarrettJacksonScraper:
    """
    Created a BarrettJacksonScraper class to scrape data from its website and stored it into CSV
    """

    def __init__(self, inventory_url):
        """
        Initalizing method
        """
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(self.script_dir)

        self.inventory_url = inventory_url

        cwd = os.path.abspath(os.getcwd())
        self.current_folder_path = os.path.join(cwd, 'Output_Folder', datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S'))

        if not os.path.exists(self.current_folder_path):
            os.makedirs(self.current_folder_path)

    def get_main_links(self):
        """
        Get links for multiple pages.
        """
        cookies = {
            'archivepage': '1',
            'OptanonAlertBoxClosed': '2023-05-12T13:07:58.541Z',
            'archivescroll': '0',
            'Favorites_hasmukh': '%5B%5D',
            'ARRAffinity': 'b2efe4ce53f5ce494bef59c180602ad420ea271b1d5'
                           '210256fa58985bba41377',
            'ARRAffinitySameSite': 'b2efe4ce53f5ce494bef59c180602ad420ea271b1d'
                                   '5210256fa58985bba41377',
            '__RequestVerificationToken': 'lBTcj0BvG_PIU747NNbVuzg9iPmDjOxv3LXN0uKnnJ1'
                                          'RAKqqp_F9136eKaYnpUUpStFbH92J1UTjwzumEqaj21KZj'
                                          '0N1Aop-IYd7A0dGGZpNdH7kUe8BuAHo7RwabO75ln_vnxpAPo'
                                          '7srf4mpMExreXcVyWbtWbcHco6PCMBSK81',
            'ASP.NET_SessionId': 'd2y5uy5rvpapyalv0mjzzvok',
            '.ASPXAUTH': '98A087EF4DAC93BB73BE192C9E56C9C736D53E74880DF'
                         '3BBD271DAB5F53B0C3DE2D40DDF0D448E0E4B46ACCE6027C6CAB3B1F5'
                         '223F483B93B361EE1E371ACD73715E51CA1BF0C102FD46A9D80E6331A'
                         '242B87C2691B919078A4C03CE8455568C677D0F94FEC582CA202F6845'
                         '8A82745AA6C7EB525E864BA2F2E545375AF7E930AE2180C28C35F63BDC7B'
                         '82280993C2A477E412E2BAA48391735E4396ED647F58',
            'OptanonConsent': 'isGpcEnabled=1&datestamp=Fri+May+19+2023+16%3A40%3A03+GMT%2B0530'
                              '+(India+Standard+Time)&version=6.37.0&isIABGlobal=false&'
                              'hosts=&consentId=6267312d-7225-4997-adcb-'
                              'f4f6d233212e&interactionCount'
                              '=2&landingPath=NotLandingPage&groups='
                              'C0004%3A0%2CC0003%3A0%2CC0002%3A0%'
                              '2CC0001%3A1&AwaitingReconsent=false&geolocation=IN%3BGJ',
        }

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/'
                      'xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Referer': 'https://www.barrett-jackson.com/Consignment/Home/Manager',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Sec-GPC': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                          '537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        res = requests.get(self.inventory_url,cookies=cookies, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        all_main_links = []
        link_founder = soup.find_all('div', class_='bj-archive-list-item')
        for i in link_founder:
            collector_car = i.find_all('div', class_='span4')[1].find('a')['href']
            id_founder = collector_car.split('/')[6:]
            id_for_page = '-'.join(id_founder)
            today = datetime.datetime.today()
            month = today.strftime('%m')
            pattern = r"\b{}-(\d{{1,2}})-2023\b".format(month)
            match = re.search(pattern, id_for_page)
            if match:
                print(id_for_page)
                url = f"https://barrettjacksoncdn.azureedge.net/staging/Content/Pages/Inventory/{id_for_page}.html"
                all_main_links.append(url)
            else:
                pass
        print(all_main_links)
        return all_main_links

    def get_inventory_links(self, main_link):
        """
        Get link of each card in each page.
        """
        # print(main_link)
        res = requests.get(url=main_link, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        all_links = []
        name_list = []
        for link in soup.find_all('h2', class_='media-heading'):
            name = link.find('a').text
            cleaned_name = re.sub(r'^Lot [\d.]+ - ', '', name)

            href = link.find('a')['href']

            link1 = f"https://www.barrett-jackson.com{href}"
            all_links.append(link1)
            name_list.append(cleaned_name)

        return all_links, name_list

    @retry(wait_exponential_multiplier=1000, wait_exponential_max=10000, stop_max_attempt_number=3)
    def fetch_inventory_details(self, link, name):
        """
        Collect details from each card.
        """
        print("we here")
        try:
            id_for_car = link.split('/')[-1].split('-')[-1]

            response = requests.get(
                f"https://barrettjacksoncdn.azureedge.net/staging/Content/Pages/InventoryDetails/{id_for_car}.html",
                timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            price_input = soup.find('input', id='hiddenprice')
            if price_input:
                price_value = price_input['value']
            else:
                price_span = soup.find('span', id='Price')
                price_value = price_span.text if price_span else ''

            price_match = re.search(r'\$(\d{1,3}(?:,\d{3})*\.\d{2})', price_value)
            price = price_match.group(1) if price_match else ''

            image_url = [i.find('img')['src'] for i in soup.find('div', class_='bj-car-carousel-items')]
            image = ' , '.join(image_url)

            details = {
                'id': id_for_car,
                'yard_number': '',
                'yard_name': '',
                'sale_date': '',
                'day_of_week': '',
                'sale_time': '',
                'time_zone': '',
                'item': name,
                'lot_number': soup.find('span', id='Lot').text if
                soup.find('span', id='Lot') else '',
                'vehicle_type': '',
                'year': soup.find('span', id='Year').text if
                soup.find('span', id='Year') else '',
                'make': soup.find('span', id='Make').text if
                soup.find('span', id='Make') else '',
                'model_group': '',
                'model_detail': soup.find('span', id='Model').text if
                soup.find('span', id='Model') else '',
                'body_style': soup.find('span', id='Style').text if
                soup.find('span', id='Style') else '',
                'color': soup.find('span', id='Exterior Color').text if
                soup.find('span', id='Exterior Color') else '',
                'damage_description':'',
                'secondary_damage':'',
                'sale_title_state':'',
                'sale_title_type':'',
                'has_keys':'',
                'lot_cond_code':'',
                'vin': f"{soup.find('span', id='VIN').text}".strip() if
                soup.find('span', id='VIN') else '',
                'odometer':'',
                'odometer_brand':'',
                'est_retail_value':'',
                'repair_cost':'',
                'engine': soup.find('span', id='Engine Size').text if
                soup.find('span', id='Engine Size') else '',
                'drive': '',
                'transmission': soup.find('span', id='Transmission').text if
                soup.find('span', id='Transmission') else '',
                'fuel_type': '',
                'cylinders': soup.find('span', id='Cylinders').text if
                soup.find('span', id='Cylinders') else '',
                'runs_drives':'',
                'sale_status':'',
                'high_bid_non_vix_sealed_vix':'',
                'special_note':'',
                'location_city':'',
                'location_state':'',
                'location_zip5':'',
                'location_zip4':'',
                'location_country':'',
                'currency_code':'',
                'image_thumbnail':image_url[0],
                'create_date_time':'',
                'grid_row':'',
                'make_an_offer_eligible':'',
                'buy_it_now_price': price,
                'image_url': image,
                'trim': '',
                'last_updated_time': '',
                'rentals': '',
                'copart_select': '',
                'source': '',
                # 'link': link,
                # 'auction': soup.find('span', id='Auction').text if
                # soup.find('span', id='Auction') else '',
                # 'reserve': soup.find('span', id='Reserve').text if
                # soup.find('span', id='Reserve') else '',
                # 'status': soup.find('span', id='Status').text if
                # soup.find('span', id='Status') else '',
                # 'interior_color': soup.find('span', id='Interior Color').text if
                # soup.find('span', id='Interior Color') else '',
                # 'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),

            }

            return details
        except Exception as e:
            print(e)

    @staticmethod
    def execution_time(function):
        """
        Decorator for execution time of any function.
        """
        if not callable(function):
            return

        @wraps(function)
        def wrapper(*args, **kwargs):
            start = time.time()
            # print(f"Function named '{function.__name__}' started")
            result = function(*args, **kwargs)
            seconds = time.time() - start
            print(f"Execution time: {seconds} seconds")
            if seconds <= 60:
                print(f"Execution time: {seconds} seconds")
            elif 60 < seconds <= 3600:
                print(f"Execution time: {seconds / 60} minutes")
            elif 3600 < seconds <= 86400:
                print(f"Execution time: {(seconds / 60) / 60} hrs")
            elif seconds > 86400:
                print(f"Execution time: {((seconds / 60) / 60) / 24} day")
            return result

        return wrapper


    @execution_time
    def scrape_inventory(self, output_file):
        """
        Scrape inventory data and store it in a CSV file, removing duplicates.
        """
        all_main_links = self.get_main_links()
        # print(len(all_main_links))
        with open(f"{self.current_folder_path}/{output_file}", 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id','yard_number','yard_name','sale_date','day_of_week',
                          'sale_time','time_zone','item','lot_number','vehicle_type',
                          'year','make','model_group','model_detail','body_style',
                          'color','damage_description','secondary_damage','sale_title_state',
                          'sale_title_type','has_keys','lot_cond_code','vin','odometer',
                          'odometer_brand','est_retail_value','repair_cost','engine','drive',
                          'transmission','fuel_type','cylinders','runs_drives','sale_status',
                          'high_bid_non_vix_sealed_vix','special_note','location_city',
                          'location_state','location_zip5','location_zip4','location_country',
                          'currency_code','image_thumbnail','create_date_time','grid_row',
                          'make_an_offer_eligible','buy_it_now_price','image_url','trim',
                          'last_updated_time','rentals','copart_select','source']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            page = 1
            unique_records = set()
            for main_link in all_main_links:
                print(f"Page no is: {page}")
                all_links, name_list = self.get_inventory_links(main_link)


                with ThreadPoolExecutor() as executor:
                    futures = []
                    for link, name in zip(all_links, name_list):
                        future = executor.submit(self.fetch_inventory_details, link, name)
                        futures.append(future)

                    for future in futures:
                        data = future.result()
                        if data['id'] not in unique_records:
                            writer.writerow(data)
                            unique_records.add(data['id'])
                page += 1


if __name__ == "__main__":
    URL = "https://www.barrett-jackson.com/Archive/Home"
    bjs_obj = BarrettJacksonScraper(URL)
    bjs_obj.scrape_inventory("Barret Jackson_image.csv")
