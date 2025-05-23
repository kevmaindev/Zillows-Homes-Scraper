import scrapy
import json
from datetime import datetime
import os

class ZilspiderSpider(scrapy.Spider):
    name = "homesspider"
    #allowed_domains = ["zillow.com"]
    url = "https://www.zillow.com/homes/New-York,-NY_rb/"

    place_folder_name = url.split('/')[-2].replace(',', '')
    today_date = datetime.today().strftime('%Y-%m-%d')
    folder_path = os.path.join('Homes Data', today_date, place_folder_name)
    
    # Ensure directory exists
    os.makedirs(folder_path, exist_ok=True)

    # Create file paths using os.path.join
    csv_path = os.path.join(folder_path, f'{place_folder_name}_Homes.csv')
    json_path = os.path.join(folder_path, f'{place_folder_name}_Homes.json')
    custom_settings = {
        'FEEDS': {
             csv_path: {
                'format': 'csv',
                'encoding': 'utf8',
                'store_empty': False,
                'fields': None,  # Replace with your fields
                'overwrite': True,
            },
            json_path : {
                'format': 'json',
                'encoding': 'utf8',
                'store_empty': False,
                'overwrite': True,
            },
        },
        'FEED_EXPORTERS': {
            'csv': 'scrapy.exporters.CsvItemExporter',
            'json': 'scrapy.exporters.JsonItemExporter',
        },
        "USER_AGENT":None,
        'DOWNLOAD_HANDLERS' : {
                "http": "scrapy_impersonate.ImpersonateDownloadHandler",
                "https": "scrapy_impersonate.ImpersonateDownloadHandler",
            },
        "TWISTED_REACTOR" : "twisted.internet.asyncioreactor.AsyncioSelectorReactor",

    }
    def start_requests(self):
        yield scrapy.Request(url=self.url,callback=self.parse,meta={"impersonate": "firefox135"})

    def parse(self, response):

        next_data_script = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()

        data = json.loads(next_data_script)

        homes = data['props']['pageProps']['searchPageState']['cat1']['searchResults']['listResults']

        for home in homes:
            broker_name = home.get('brokerName', None)
            if broker_name is not None:
                broker_name = broker_name.strip('Listing by:')

            home_data = {
                "home_type": home['hdpData']['homeInfo'].get('homeType', None),
                "posted": str(home['hdpData']['homeInfo'].get('daysOnZillow', None)) + ' days ago',
                "Broker Name": broker_name,
                "home_status": home.get('statusType', None),
                "home_price": home.get('price', None),
                "home_address": home.get('address', None),
                "home_zipcode": home.get('addressZipcode', None),
                "num_beds": home.get('beds', None),
                "num_baths": home.get('baths', None),
                "home_area": home.get('area', None),
                "home_URL": home.get('detailUrl', None),
                "home_main_image": home.get('imgSrc', None),
            }

            yield home_data

        next_page_url = data['props']['pageProps']['searchPageState']['cat1']['searchList']['pagination'].get('nextUrl',None)

        if (next_page_url):
            next_page_full_url ='https://www.zillow.com/homes' + next_page_url
            yield scrapy.Request(url=next_page_full_url,callback=self.parse,meta={"impersonate": "firefox135"})
        