import datetime
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

cwd = os.path.abspath(os.getcwd())
folder_name = os.path.join(cwd, 'Output_folder',
                        datetime.now().strftime('%Y-%m-%d_%H_%M_%S'))
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

today = datetime.datetime.today()
formatted_date = today.strftime("%m-%d-%Y")

cookies = {
    '_gcl_au': '1.1.2057298493.1684690920',
    '_fbp': 'fb.1.1684690921415.648044857',
    'intercom-id-z6wzvfvh': '7c1fec42-ed0b-422b-99e8-c878113d1be5',
    'intercom-device-id-z6wzvfvh': 'fa84ab8e-2034-4ba2-8370-cc9703603232',
    '_hjSessionUser_1737318': 'eyJpZCI6ImRmNmQzMGFlLTg5MDAtNTdkMC05NTIwLWIyMDVkZTI1YjQ2NCIsImNyZWF0ZWQiOjE2ODQ2OTA5MjAxMTgsImV4aXN0aW5nIjp0cnVlfQ==',
    'destination_country': 'US',
    'destination_zip_to': '07101',
    'destination_zip_to_description': 'Newark%2C+NJ',
    'intercom-session-z6wzvfvh': '',
    'g_state': '{"i_p":1688639361820,"i_l":3}',
    'PHPSESSID': '4m2htlelho4k7oaj7jkfcm1umr',
    '_gid': 'GA1.2.1678532953.1688442184',
    '_ga_726TE0SKY8': 'GS1.2.1688454059.5.1.1688455173.60.0.0',
    'search_params': 'search_type%3Dsearch%26searchParams%3Dtype-cars%252Fmake-ford',
    '_ga': 'GA1.1.49865247.1684690920',
    '_uetsid': 'e1b5d1a01a1c11eea5cf39b0df591a9a',
    '_uetvid': 'ca66b110f7fe11eda479693f253be02a',
    '_ga_50ZR963YM6': 'GS1.1.1688454058.11.1.1688457705.58.0.0',
    '__language': 'en',
}

headers = {
            'authority': 'sca.auction',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'en-US,en;q=0.5',
            'sec-ch-ua': '"Brave";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'sec-gpc': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        }
params = {
    'saleDateFrom': formatted_date,
    'saleDateTo': formatted_date,
    'sort': 'sale_date',
    'page': '1',
    'isLocationPage': '0',
}

vehicle_headers = {
    'authority': 'sca.auction',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67',
}
