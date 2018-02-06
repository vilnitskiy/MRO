# -*- coding: utf-8 -*-
import pandas as pd
import scrapy


class BaseMroSpider(scrapy.Spider):
    search_url = '' #example https://www.patriot-supply.com/?q={}
    path_to_data = '' 
    separator = ',' # , or ; or something
    fields = [] #felds in csv file withou catalog_number
    base_cookies = {}


    def __init__(self, *args, **kwargs):
        super(BaseMroSpider, self).__init__(*args, **kwargs)
        data = pd.read_csv(self.path_to_data, sep=self.separator)
        self.catalog = list(data.catalog_number)
        for field in set(self.fields):
            setattr(self, 'catalog_' + field, dict(zip(self.catalog, map(lambda x: str(x), getattr(data, field, '')))))

    def start_requests(self):
        for row in self.catalog:
            yield scrapy.Request(url=self.search_url.format(row),
                                 callback=self.parse_item,
                                 cookies=self.base_cookies,
                                 meta={'row': row})
