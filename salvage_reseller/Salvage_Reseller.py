"""
This module are used to scrapes the cars information from a website and saves it to a CSV file.

"""
import os
import datetime
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

print(__doc__) # prints the functionlity of the module using doc string

class Salvage:
    "This class is used to initialize page1, page2, to_url, count, result, cookies, headers values"
    # Inorder to print the functionlity of the class using doc string print it outside the class
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(self.script_dir)

        self.page1 = 0
        self.page2 = 25
        self.to_url = set()
        self.count = 1
        self.result = []


        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Referer': f'https://www.salvagereseller.com/cars-for-sale/type/automobiles/page/{self.page1}/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

    def create_output_folder(self):
        """
        Creating a output folder to write the content
        """
        cwd = os.path.abspath(os.getcwd())
        self.folder_name = os.path.join(cwd, 'Output_folder',
                            datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S'))
        if not os.path.exists(self.folder_name):
            os.makedirs(self.folder_name)

    def scrape_urls(self):
        "This function is used to pull all the urls from the website and store in a list"
        print(self.scrape_urls.__doc__) # doc string tell about the functionlity
        upd_page1 = self.page1
        while True:
            print('Starting scrape_urls method...')
            headers = self.headers
            print(headers['Referer'])
            rurl = headers['Referer'].replace(str(upd_page1), str(self.page2))
            print(rurl)
            session = requests.Session()
            response = session.get(
                rurl,

                headers=headers,
                timeout=10  # this is used to wait till 10 seconds for server to respond, if it doesn't
            )
            res = response.json()
            lis = res['listing']
            soup = BeautifulSoup(lis, 'html.parser')
            href = soup.select('div.my-4.vehicle-row.position-relative a.vehicle-model')
            if not href:   # It is going to break the loop once there are no urls found
                break
            # print(href)
            for hre in href:
                result = hre.get('href')
                if result not in self.to_url:
                    print(self.count, result)
                    self.to_url.add(result)
                    self.count = self.count + 1
            upd_page1 += 25
            headers['Referer'] = f'https://www.salvagereseller.com/cars-for-sale/type/automobiles/page/{upd_page1}'
            self.page2 += 25
            if self.count >= 3000:
                break
        print(len(self.to_url))

    def cars_info(self):
        "This function is used to get all the information from each url and store it in dictionary"
        filename = f"{self.folder_name}/Salvage_reseller.csv"
        print(self.cars_info.__doc__) # doc string tell about the functionality
        for p_url in self.to_url:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            }
            max_attempt = 3
            while True:
                attempt = 1
                while attempt <= max_attempt:
                    try:
                        time.sleep(3)
                        session = requests.Session()
                        retry = Retry(total=max_attempt, backoff_factor=0.5) # status_forcelist=[500, 502, 503, 504, 443]
                        adapter = HTTPAdapter(max_retries=retry)
                        session.mount('http://', adapter)
                        session.mount('https://', adapter)
                        resp = session.get(p_url, headers=headers, timeout=30)
                        # Process the response and break the loop if successful
                        break
                    except requests.exceptions.Timeout:
                        print(f"Timeout occurred. Retrying request ({attempt}/{max_attempt})...")
                        attempt += 1
                        time.sleep(60)  # Wait for 5 seconds before retrying
                if attempt > max_attempt:
                    print("Maximum number of attempts reached. Unable to complete the request.")
                    # Handle the error condition or exit the program
                    continue # Restart the loop from the beginning
                break
            soup1 = BeautifulSoup(resp.content, 'html.parser')
            # try:
            #     div = soup1.find('div', text='Actual Cash Value:')
            #     value_div = div.find_next_sibling('div')
            #     value = value_div.text.strip()
            # except (AttributeError, TypeError):
            #     value = "NA"
            try:
                div20 = soup1.find('div', text='Sale Date:')
                value_div20 = div20.find_next_sibling('div')
                value20 = value_div20.text.strip()
            except (AttributeError, TypeError):
                value20 = "NA"

            current_date = datetime.date.today()

            # Format the date as 'MM/DD/YYYY'
            formatted_date = current_date.strftime('%m/%d/%Y')
            print(f"formatted {formatted_date} value20: {value20}")
            if value20 == "Upcoming Lot":
                pass
            else:
                try:
                    div1 = soup1.find('div', text='Buy It Now Price:')
                    value_div1 = div1.find_next_sibling('div')
                    value1 = value_div1.text.strip()
                except (AttributeError, TypeError):
                    value1 = "NA"
                # try:
                #     div2 = soup1.find('div', text='Title State/Type:')
                #     value_div2 = div2.find_next('span')
                #     value2 = value_div2.text.strip()
                # except (AttributeError, TypeError):
                #     value2 = "NA"
                try:
                    div3 = soup1.find('div', text='Odometer:')
                    value_div3 = div3.find_next_sibling('div')
                    value3 = value_div3.text.strip()
                except (AttributeError, TypeError):
                    value3 = "NA"
                # try:
                #     div4 = soup1.find('div', text='Primary Damage:')
                #     value_div4 = div4.find_next_sibling('div')
                #     value4 = value_div4.text.strip()
                # except (AttributeError, TypeError):
                #     value4 = "NA"
                try:
                    div5 = soup1.find('div', text='Secondary Damage:')
                    value_div5 = div5.find_next_sibling('div')
                    value5 = value_div5.text.strip()
                except (AttributeError, TypeError):
                    value5 = "NA"
                try:
                    div6 = soup1.find('div', class_="card mb-3 border-0")
                    value_div6 = div6.find('div', class_="card-body p-0")
                    value_divv6 = value_div6.find('a')
                    value6 = value_divv6['href'].split("https://www.salvagereseller.com/vin-history?vin=")[1]
                except (AttributeError, TypeError):
                    value6 = "NA"
                try:
                    div7 = soup1.find('div', text='Color:')
                    value_div7 = div7.find_next_sibling('div')
                    value7 = value_div7.text.strip()
                except (AttributeError, TypeError):
                    value7 = "NA"
                try:
                    div8 = soup1.find('div', text='Engine:')
                    value_div8 = div8.find_next_sibling('div')
                    value8 = value_div8.text.strip()
                except (AttributeError, TypeError):
                    value8 = "NA"
                try:
                    div9 = soup1.find('div', text='Cylinders:')
                    value_div9 = div9.find_next_sibling('div')
                    value9 = value_div9.text.strip()
                except (AttributeError, TypeError):
                    value9 = "NA"
                try:
                    div10 = soup1.find('div', text='Drive:')
                    value_div10 = div10.find_next_sibling('div')
                    value10 = value_div10.text.strip()
                except (AttributeError, TypeError):
                    value10 = "NA"
                try:
                    div11 = soup1.find('div', text='Transmission:')
                    value_div11 = div11.find_next_sibling('div')
                    value11 = value_div11.text.strip()
                except (AttributeError, TypeError):
                    value11 = "NA"
                try:
                    div12 = soup1.find('div', text='Fuel:')
                    value_div12 = div12.find_next_sibling('div')
                    value12 = value_div12.text.strip()
                except (AttributeError, TypeError):
                    value12 = "NA"
                try:
                    div13 = soup1.find('div', text='Keys:')
                    value_div13 = div13.find_next_sibling('div')
                    value13 = value_div13.text.strip()
                except (AttributeError, TypeError):
                    value13 = "NA"
                # try:
                #     div14 = soup1.find('div', text='Seller:')
                #     value_div14 = div14.find_next_sibling('div')
                #     value14 = value_div14.text.strip()
                # except (AttributeError, TypeError):
                #     value14 = "NA"
                # try:
                #     div15 = soup1.find('div', text='Highlights:')
                #     value_div15 = div15.find_next('div')
                #     value15 = value_div15.text.strip()
                #     span15 = value_div15.find('span')
                #     span15.extract() # remove the span tag, here span will be removed
                #     value15 = value_div15.text.strip()
                # except (AttributeError, TypeError):
                #     value15 = "NA"
                # try:
                #     value16 = p_url
                # except (AttributeError, TypeError):
                #     value16 = "NA"
                # value17 = ""
                value18 = ""
                value19 = ""
                value21 = ""
                try:

                    div22 = soup1.find('div', text='Virtual Sale Time:')
                    value_div22 = div22.find_next_sibling('div')
                    value22 = value_div22.text.strip()
                except (AttributeError, TypeError):
                    value22 = "NA"
                value23 = ""
                try:
                    value24 = soup1.find('h1').text.strip()
                except (AttributeError, TypeError):
                    value24 = "NA"
                value25 = ""
                value26 = ""
                value27 = ""
                value28 = ""
                value29 = ""
                value30 = ""
                value31 = ""
                try:
                    div32 = soup1.find('div', text='Sale Name:')
                    value_div32 = div32.find_next_sibling('div')
                    value32 = value_div32.text.strip()
                except (AttributeError, TypeError):
                    value32 = "NA"
                value33 = ""
                value34 = ""
                value35 = ""
                value36 = ""
                value37 = ""
                value38 = ""
                try:
                    div39 = soup1.find('div', text='Sale Status:')
                    value_div39 = div39.find_next_sibling('div')
                    value39 = value_div39.text.strip()
                except (AttributeError, TypeError):
                    value39 = "NA"
                value40 = ""
                value41 = ""
                value42 = ""
                value43 = ""
                value44 = ""
                value45 = ""
                value46 = ""
                try:
                    div47 = soup1.find('div', text='Actual Cash Value:')
                    value_div47 = div47.find_next_sibling('div')
                    value47 = value_div47.text.strip()[-3:]
                except (AttributeError, TypeError):
                    value47 = "NA"
                try:
                    value_48 = soup1.find('div', class_="photo-swipe").img
                    value48 = value_48.get('src')
                except (AttributeError, TypeError):
                    value48 = "NA"
                value49 = ""
                value50 = ""
                value51 = ""
                try:
                    value52 = []
                    value123 = soup1.find('div', class_="gallery")
                    value_123 = value123.find_all('div', class_="d-flex align-content-stretch justify-content-center flex-wrap r1ow")
                    for value_22 in value_123:
                        anchor_tags = value_22.find_all('a', class_="flex-grow-1 change_image")
                        for anchor_tag in anchor_tags:
                            href = anchor_tag.get('href')
                            value52.append(href)
                except (AttributeError, TypeError):
                    value52 = "NA"
                value53 = ""
                value54 = ""
                value55 = ""
                value56 = ""
                value57 = ""

                # Store the information in a dictionary
                info = {
                    #'Actual Cash Value':value,
                    'Item':value24,
                    'Buy It Now Price':value1,
                    #'Title State/Type':value2,
                    'Odometer':value3,
                    #'Primary Damage':value4,
                    'Secondary Damage':value5,
                    'VIN':value6,
                    'Color':value7,
                    'Engine':value8,
                    'Cylinders':value9,
                    'Drive':value10,
                    'Transmission':value11,
                    'Fuel':value12,
                    'Keys':value13,
                    #'Seller':value14,
                    #'Highlights':value15,
                    #'Vehicle URL':value16,
                    'Sale Date' : value20,
                    'Sale Title State': value32,
                    'Sale Status': value39,
                    'Sale Time': value22,
                    'Currency Code': value47,
                    'Image Thumbnail': value48,
                    'Image URL': value52,
                    'Day_of_week': value21,
                    # 'Id': value17,
                    'Yard Number': value18,
                    'Yard Name': value19,
                    'Time Zone': value23,
                    'Vehicle Type': value25,
                    'Year': value26,
                    'Make': value27,
                    'Model Group': value28,
                    'Model Detail': value29,
                    'Body Style': value30,
                    'Damage Description': value31,
                    'Sale Title Type': value33,
                    'Lot Cond Code': value34,
                    'Odometer Brand': value35,
                    'Est Retail Value': value36,
                    'Repair Cost': value37,
                    'Runs Drives': value38,
                    'High bid non vix sealed vix': value40,
                    'Special Note': value41,
                    'Location City': value42,
                    'Location State': value43,
                    'Location Zip5': value44,
                    'Location Zip4': value45,
                    'Location Country': value46,
                    'Create Date Time': value49,
                    'Grid Row': value50,
                    'Make an offer eligible': value51,
                    'Trim': value53,
                    'Last Updated Time': value54,
                    'Rentals': value55,
                    'Copart Select': value56,
                    'Lot Number': value57,

                    }
                self.result.append(info)
                # Convert the list of dictionaries to a Pandas DataFrame
                # Create a DataFrame from the 'info' dictionary
                data_frame = pd.DataFrame([info])

                # Append the data to the CSV file
                if os.path.isfile(filename):
                    # Append the data to the CSV file
                    data_frame.to_csv(filename, mode='a', header=False, index=False)
                else:
                    # If the file doesn't exist, create it and write the data
                    data_frame.to_csv(filename, index=False)

if __name__ == '__main__':
    t1 = time.time()
    obj = Salvage()
    print(obj.__doc__) # it prints the functionality of the class using doc string
    obj.create_output_folder()
    obj.scrape_urls()
    obj.cars_info()
    print("Scrapped the urls")
    print(f'Time taken to scrape all {len(obj.to_url)} is : {time.time()-t1}s')