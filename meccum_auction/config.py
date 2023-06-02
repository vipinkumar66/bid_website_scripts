import os
from datetime import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

cwd = os.path.abspath(os.getcwd())
folder_name = os.path.join(cwd, 'Output_folder',
                        datetime.now().strftime('%Y-%m-%d_%H_%M_%S'))
if not os.path.exists(folder_name):
    os.makedirs(folder_name)


auction_url = ('https://ignition.mecumauctions.com/graphql?query=query%20'
                'GET_AUCTIONS_BY_META(%24first%3A%20Int%2C%20%24where%3A%2'
                '0RootQueryToAuctionConnectionWhereArgs%2C%20%24hasPaginat'
                'ion%3A%20Boolean%20%3D%20false)%20%7B%0A%20auctions(first'
                '%3A%20%24first%2C%20where%3A%20%24where)%20%7B%0A%20pageI'
                'nfo%20%40include(if%3A%20%24hasPagination)%20%7B%0A%20off'
                'setPagination%20%7B%0A%20total%0A%20__typename%0A%20%7D%0'
                'A%20__typename%0A%20%7D%0A%20edges%20%7B%0A%20node%20%7B%'
                '0A%20id%0A%20auctionFields%20%7B%0A%20auctionStartDate%0A'
                '%20auctionEndDate%0A%20auctionSubtitle%0A%20positionReque'
                'stForm%20%7B%0A%20mediaItemUrl%0A%20__typename%0A%20%7D%0'
                'A%20__typename%0A%20%7D%0A%20hasLots%0A%20registrationsCo'
                'nsignments%20%7B%0A%20nodes%20%7B%0A%20slug%0A%20__typena'
                'me%0A%20%7D%0A%20__typename%0A%20%7D%0A%20title%0A%20slug'
                '%0A%20uri%0A%20featuredImage%20%7B%0A%20node%20%7B%0A%20a'
                'ltText%0A%20mediaDetails%20%7B%0A%20height%0A%20width%0A%'
                '20__typename%0A%20%7D%0A%20mediaItemUrl%0A%20__typename%0'
                'A%20%7D%0A%20__typename%0A%20%7D%0A%20__typename%0A%20%7D'
                '%0A%20__typename%0A%20%7D%0A%20__typename%0A%20%7D%0A%7D&'
                'operationName=GET_AUCTIONS_BY_META&variables=%7B%22hasPag'
                'ination%22%3Afalse%2C%22first%22%3A28%2C%22where%22%3A%7B'
                '%22metaQuery%22%3A%7B%22metaArray%22%3A%5B%7B%22key%22%3A'
                '%22auction_start_date%22%7D%2C%7B%22key%22%3A%22auction_e'
                'nd_date%22%2C%22compare%22%3A%22GREATER_THAN_OR_EQUAL_TO%'
                '22%2C%22value%22%3A%2220230513%22%2C%22type%22%3A%22DATE%'
                '22%7D%5D%7D%2C%22orderby%22%3A%7B%22orderby%22%3A%7B%22fi'
                'eld%22%3A%22AUCTION_START_DATE%22%2C%22order%22%3A%22ASC%'
                '22%7D%7D%7D%7D')

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
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                              ' (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
                'content-type': 'application/x-www-form-urlencoded',
                'sec-ch-ua': '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
            }