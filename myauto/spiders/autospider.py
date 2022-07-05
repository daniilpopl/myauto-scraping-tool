from typing import Iterable, Text
from urllib import response
import scrapy
from scrapy import Spider
from scrapy.http import TextResponse
from scrapy.selector import Selector
from scrapy.exceptions import CloseSpider
import re
import requests
from tqdm.auto import tqdm

MAX_PAGES = 10279
page_num_pat = re.compile(r'\d+')
class MyAutoSpider(Spider):
    name = 'myauto'

    def start_requests(self):
        start_urls = [f'https://api2.myauto.ge/en/products?Page={n}' 
                    for n in range(1, MAX_PAGES)]
        for url in tqdm(start_urls):
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: TextResponse):
        car_items = response.json()['data']['items']

        for car_item in car_items:
            api_url = f"https://api2.myauto.ge/en/products/{car_item['car_id']}"
            yield response.follow(
                url=api_url, 
                callback=self.parse_statement, 
                cb_kwargs=dict(statement_card = car_item),
            )

        # pagination_links = response.css('li.next a')
        # next_url = page_num_pat.findall(response.url)[0]
        # yield from response.follow_all(pagination_links, self.parse)

    def parse_statement(self, response: TextResponse, statement_card: dict = None):

        image_url_format = ''
        # Also add images

        # img_path = "/".join(list(num[::-1][:5]))
        data = {}
        api_response = response.json()
        try:
            del api_response['data']['info']['matching_parts'] # Remove product offers
        except:
            pass # Ignore
        data['inner_api_call'] = api_response['data']# Response has to be json

        data['statemet_card'] = statement_card

        data['meta_data'] = dict(
            url=response.url,
            image_dir=f'{statement_card["car_id"]}', # added in the future!
        )

        # img_resp = requests.get(
        #     url=f"https://static.my.ge/myhome/photos/{img_path}/thumbs/{num}_{n}.jpg",
        #     headers={
        #     "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"102\", \"Google Chrome\";v=\"102\"",
        #     "sec-ch-ua-mobile": "?0",
        #     "sec-ch-ua-platform": "\"Linux\"",
        #     "Referer": "https://www.myhome.ge/",
        #     "Referrer-Policy": "strict-origin-when-cross-origin"
        #     },
        # )
        # img_data = img_resp.content
        # with open('image_name.jpg', 'wb') as handler:
        #     handler.write(img_data)
        # for key in data.keys():
        #     vals = []
        #     for v in vals: statement_page.css(data[key]).getall()

        # def strip_recursive(s):
        #     if isinstance(s, str):
        #         s = s.strip()
        #         s = re.sub(r'\t+',' ',s)
        #         return s
        #     if isinstance(s, dict):
        #         return dict({k:strip_recursive(v) for k,v in s.items()})
        #     if isinstance(s, (list, tuple)):
        #         return tuple(strip_recursive(v) for v in s)

        # # data = {k: tuple(str_prep(s) ) for k,v in selectors.items()}
        # data = strip_recursive(data)

        yield  data 