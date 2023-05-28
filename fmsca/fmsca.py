"""Importing Required Libraries"""
import os
import csv
import datetime
import zipfile
import urllib.request
import requests
import pandas as pd
from bs4 import BeautifulSoup


class ZipCsv:

    """Downloading Zip from website and converting that to the structured CSV"""

    def __init__(self):

        """Initalizng current directory"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)

        cwd = os.path.abspath(os.getcwd())
        self.current_folder = os.path.join(cwd, 'Output_folder', datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S'))

        if not os.path.exists(self.current_folder):
            os.makedirs(self.current_folder)

    def get_file(self):

        """Downlaoding the Zip file from the website"""

        headers = {
            'authority': 'ai.fmcsa.dot.gov',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                      'image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Microsoft Edge";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
        }

        response = requests.get('https://ai.fmcsa.dot.gov/SMS/Tools/Downloads.aspx',
                                headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        links = soup.find_all('ul', class_='downloadLinks')

        motor_carrier_inspection_information = links[-3].find('a').get('href')
        motor_carrier_crash_information = links[-2].find('a').get('href')

        url1 = f'{motor_carrier_crash_information}'
        filename1 = f'{self.current_folder}/{motor_carrier_crash_information.split("/")[-1]}'
        urllib.request.urlretrieve(url1, filename1)

        url2 = f'{motor_carrier_inspection_information}'
        filename2 = f'{self.current_folder}/{motor_carrier_inspection_information.split("/")[-1]}'
        urllib.request.urlretrieve(url2, filename2)

        self.extract_zip(filename1, filename2)
        self.txt_to_csv(filename1, filename2)

    def extract_zip(self, filename1, filename2):

        """Extracting a zip file"""

        with zipfile.ZipFile(filename1, 'r') as zip_ref:
            zip_ref.extractall(f'{self.current_folder}')

        with zipfile.ZipFile(filename2, 'r') as zip_ref:
            zip_ref.extractall(f'{self.current_folder}')

    def txt_to_csv(self, filename1, filename2):

        """Converting TXT file to CSV"""

        zip_name1 = f'{filename1.split("_")[-1].replace(".zip", "")}_Crash'
        print(zip_name1)
        with open(f'{self.current_folder}/{zip_name1}.txt', 'r', encoding='latin-1') as input_file:
            with open(f'{self.current_folder}/{zip_name1}.csv', 'w', newline='', encoding='latin-1') as output_file:
                writer = csv.writer(output_file, delimiter=',',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for line in input_file:
                    row = line.strip().replace('"', "'").replace(',', ';')
                    writer.writerow(row.split(';'))

        zip_name2 = f'{filename2.split("_")[-1].replace(".zip", "")}_Inspection'
        print(zip_name2)
        with open(f'{self.current_folder}/{zip_name2}.txt', 'r', encoding='latin-1') as input_file:
            with open(f'{self.current_folder}/{zip_name2}.csv', 'w', newline='', encoding='latin-1') as output_file:
                writer = csv.writer(output_file, delimiter=',',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for line in input_file:
                    row = line.strip().replace('"', "'").replace(',', ';')
                    writer.writerow(row.split(';'))

        self.filter_csv(zip_name1, zip_name2)

    def filter_csv(self, zip_name1, zip_name2):

        """Mapping columns which are needed to the new CSV"""

        df1 = pd.read_csv(f'{self.current_folder}/{zip_name1}.csv', encoding='latin-1', error_bad_lines=False)
        columns_of_interest1 = ["'REPORT_NUMBER'", "'REPORT_DATE'", "'REPORT_STATE'",
                                "'VEHICLE_ID_NUMBER'", "'VEHICLE_LICENSE_STATE'"]
        filtered_df1 = df1[columns_of_interest1]
        filtered_df1.columns = [col.replace('\'', '') for col in filtered_df1.columns]
        filtered_df1 = filtered_df1.\
            applymap(lambda x: x.replace("'", "") if isinstance(x, str) else x)
        filtered_df1.to_csv(f'filtered_{zip_name1}.csv', index=False)

        df2 = pd.read_csv(f'{self.current_folder}/{zip_name2}.csv', encoding='latin-1', error_bad_lines=False)
        columns_of_interest2 = ["'REPORT_NUMBER'", "'REPORT_STATE'", "'INSP_DATE'",
                                "'UNIT_MAKE'", "'UNIT_LICENSE_STATE'", "'VIN'",
                                "'UNIT_MAKE2'", "'UNIT_LICENSE_STATE2'", "'VIN2'"]
        filtered_df2 = df2[columns_of_interest2]
        filtered_df2.columns = [col.replace('\'', '') for col in filtered_df2.columns]
        filtered_df2 = filtered_df2.\
            applymap(lambda x: x.replace("'", "") if isinstance(x, str) else x)
        filtered_df2.to_csv(f'{self.current_folder}/filtered_{zip_name2}.csv', index=False)


obj = ZipCsv()
obj.get_file()
