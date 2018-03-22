# -*- coding: utf-8 -*-
import json
import re
import pandas as pd
import scrapy
from mro.BaseSpiders.base_spiders import BaseMroSpider


class Martin(BaseMroSpider):
    name = "jasonbymegadyne_img"
    search_url = 'http://rubberproducts.jasonbymegadyne.com/keyword/all-categories?key=all&&keyword={}&SchType=2'
    path_to_data = 'mro/spiders/csv_data/jasonbymegadyne/(Jason Industrial without main_image) Product_2018-3-19.csv'
    separator = ','
    output_fields = ('id', 'catalog_number', 'img')

    def parse_item(self, resp):
        if '/item/' in resp.url:
            catalog = resp.meta['row']
            return self.create_item(
                self.catalog_id[catalog],
                catalog,
                resp.urljoin(resp.xpath('//img[@itemprop="image"]/@src').extract_first() or 1/0) # to initiate exception
                )





