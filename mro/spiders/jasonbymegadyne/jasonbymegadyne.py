# -*- coding: utf-8 -*-
import json
import re
import pandas as pd
import scrapy
from mro.BaseSpiders.base_spiders import BaseMroSpider


class Martin(BaseMroSpider):
    name = "jasonbymegadyne"
    search_url = 'http://rubberproducts.jasonbymegadyne.com/keyword/all-categories?key=all&&keyword={}&SchType=2'
    path_to_data = 'mro/spiders/csv_data/jasonbymegadyne/(Jason Industrial) Product_2018-3-19.csv'
    separator = ','
    output_fields = ('id', 'catalog_number', 'description', 'specifications')

    def parse_item(self, response):
        if '/item/' in response.url:
            catalog = response.meta['row']
            description = response.xpath('//div[@itemprop="description"]').extract_first() or ''
            specs = ''
            for tr in response.xpath('//a[@name="Specifications"]/..//table[@class="plp-item-table"]/tbody/tr'):
                k = (tr.xpath('./td[1]/h2/strong/text()').extract_first() or \
                    tr.xpath('./td[1]/strong/text()').extract_first()).strip().encode('utf-8')
                v = ' '.join(tr.xpath('./td[2]/span/span[2]/span/text()').extract()).encode('utf-8')
                specs += '{}:{}|'.format(k,v)
            return self.create_item(self.catalog_id[catalog], catalog, description, specs[:-1] if specs else '')





