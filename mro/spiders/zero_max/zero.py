# -*- coding: utf-8 -*-
import json
import re
import pandas as pd
import scrapy
from mro.BaseSpiders.base_spiders import BaseMroSpider
from mro.items import UniversalItem



class Martin(BaseMroSpider):
    name = "zero"
    search_url = 'https://www.zero-max.com/custom_search.php?keywords={}&type=All'
    path_to_data = 'mro/spiders/csv_data/zero/Zero-Max.csv'
    separator = ','
    fields = ['id']
    base_cookies = {
    'cds.catalog.unit': 'metric'
    }


    def parse_item(self, response):
        catalog = response.meta['row']
        if 'product_info' in response.url:
            attr = ''
            for tr in response.xpath('//*[@id="cds-product-attribute-table"]/tbody/tr'):
                attr += tr.xpath('./td[1]/text()').extract_first() + ':' + tr.xpath('./td[2]/text()').extract_first() + '|'
            return {
             'id': self.catalog_id[catalog],
             'catalog_number': catalog,
             'attributes': attr[:-1] if attr else ''
            }



