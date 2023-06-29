import os
from datetime import datetime
from fake_useragent import UserAgent

useragent = UserAgent()

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

cwd = os.path.abspath(os.getcwd())
folder_name = os.path.join(cwd, 'Output_folder',
                        datetime.now().strftime('%Y-%m-%d_%H_%M_%S'))
if not os.path.exists(folder_name):
    os.makedirs(folder_name)


auction_url = (
    'https://ignition.mecumauctions.com/graphql?query=query%20GET_AUCTIONS_BY_DATE(%24date%3A%20String!%2C%20%24first%3A%20Int)%20%7B%0A%20auctions(%0A%20first%3A%20%24first%0A%20where%3A%20%7BmetaQuery%3A%20%7BmetaArray%3A%20%5B%7Bkey%3A%20%22auction_start_date%22%7D%2C%20%7Bvalue%3A%20%24date%2C%20key%3A%20%22auction_end_date%22%2C%20compare%3A%20GREATER_THAN_OR_EQUAL_TO%2C%20type%3A%20DATE%7D%5D%7D%2C%20orderby%3A%20%7Bfield%3A%20AUCTION_START_DATE%2C%20order%3A%20ASC%7D%7D%0A%20)%20%7B%0A%20edges%20%7B%0A%20node%20%7B%0A%20id%0A%20auctionFields%20%7B%0A%20auctionStartDate%0A%20auctionEndDate%0A%20__typename%0A%20%7D%0A%20title%0A%20slug%0A%20uri%0A%20featuredImage%20%7B%0A%20node%20%7B%0A%20altText%0A%20mediaDetails%20%7B%0A%20height%0A%20width%0A%20__typename%0A%20%7D%0A%20mediaItemUrl%0A%20__typename%0A%20%7D%0A%20__typename%0A%20%7D%0A%20__typename%0A%20%7D%0A%20__typename%0A%20%7D%0A%20__typename%0A%20%7D%0A%7D&operationName=GET_AUCTIONS_BY_DATE&variables=%7B%22date%22%3A%2220230629%22%2C%22first%22%3A4%7D'
    )

auction_data_headers ={
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.7',
                'Connection': 'keep-alive',
                'Origin': 'https://www.mecum.com',
                'Referer': 'https://www.mecum.com/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
                'Sec-GPC': '1',
                'User-Agent': useragent.random,
                'content-type': 'application/x-www-form-urlencoded',
                'sec-ch-ua': '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
            }

headers = ['yard_number', 'yard_name', 'sale_date', 'day_of_week', 'sale_time', 'time_zone', 'item',
            'lot_number', 'vehicle_type', 'year', 'make', 'model_group', 'model_detail', 'body_style', 'color',
            'damage_description', 'secondary_damage', 'sale_title_state', 'sale_title_type', 'has_keys',
            'lot_cond_code', 'vin', 'odometer', 'odometer_brand', 'est_retail_value', 'repair_cost', 'engine',
            'drive', 'transmission', 'fuel_type', 'cylinders', 'runs_drives', 'sale_status',
            'high_bid_non_vix_sealed_vix',
            'special_note', 'location_city', 'location_state', 'location_zip5', 'location_zip4',
            'location_country', 'currency_code', 'image_thumbnail', 'create_date_time', 'grid_row',
            'make_an_offer_eligible', 'buy_it_now_price', 'image_url', 'trim', 'last_updated_time', 'rentals',
            'copart_select', 'source', 'Timestamp']

