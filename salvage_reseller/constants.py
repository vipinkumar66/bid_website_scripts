import os
import datetime


script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)


cwd = os.path.abspath(os.getcwd())
folder_name = os.path.join(cwd, 'Output_folder',
                    datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S'))
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
filename = f"{folder_name}/Salvage_reseller.csv"

import requests

cookies = {
    '_gcl_au': '1.1.1937931851.1685254497',
    '_fbp': 'fb.1.1685254497004.459514322',
    '_ga': 'GA1.2.1776967408.1685254497',
    'IR_gbd': 'salvagereseller.com',
    '_gid': 'GA1.2.1701265035.1688356295',
    'cebs': '1',
    '_ce.clock_event': '1',
    '_ce.clock_data': '512%2C122.50.228.44%2C1%2Cc22c6b1174b8b2e448bbba9ffe8ddfb7',
    'hide-filters': '0',
    'ci_session': 'g5p2djcnsm5fut9oqmfl3tdknpvjqkvb',
    'IR_19452': '1688359703126%7C0%7C1688359703126%7C%7C',
    '__gads': 'ID=c6fad636dd3ecbe8-22fc5f7b8ce1003e:T=1685254494:RT=1688359704:S=ALNI_MaJvtBknbdturYZaBTX847fd4BocQ',
    '__gpi': 'UID=00000c0bd18123a2:T=1685254494:RT=1688359704:S=ALNI_MbpI1J4x3LeSSbN7MHnuGeehM2yrA',
    'cebsp_': '16',
    '_ce.s': 'v~8bf7b12f558c2a36b58a5731b420b07a5a8c9b64~lcw~1688356733846~vpv~1~v11.rlc~1688359712175~lcw~1688359712177',
    '_uetsid': 'e8106810195411ee96001542bc6dc7f4',
    '_uetvid': 'f85a6f70fd1e11edae2b8f60ca41daaf',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Referer': 'https://www.salvagereseller.com/cars-for-sale/sale-date/2023-07-03?page=25',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': '',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}
