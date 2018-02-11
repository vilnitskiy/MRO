# -*- coding: utf-8 -*-
import pandas as pd
import scrapy


class BaseMroSpider(scrapy.Spider):
    search_url = '' #example https://www.patriot-supply.com/?q={}
    path_to_data = '' 
    separator = ',' # , or ; or something
    #exclude_fields = [] #exclude fields
    base_cookies = {}
    output_fields = ()

    def __init__(self, *args, **kwargs):
        super(BaseMroSpider, self).__init__(*args, **kwargs)
        data = pd.read_csv(self.path_to_data, sep=self.separator)
        self.catalog = data.catalog_number
        #for field in set(data._data.items) - set(self.exclude_fields) - set('catalog_number'):
        for field in set(data._data.items) - set('catalog_number'):
            setattr(self, 'catalog_' + field, dict(zip(self.catalog, map(str, getattr(data, field, '')))))

    def create_item(self, *args):
    	return dict(zip(self.output_fields, args))

    def start_requests(self):
        for row in self.catalog:
            yield scrapy.Request(url=self.search_url.format(row),
                                 callback=self.parse_item,
                                 cookies=self.base_cookies,
                                 meta={'row': row})
