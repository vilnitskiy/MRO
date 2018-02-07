# -*- coding: utf-8 -*-
import json
import re
import pandas as pd
import scrapy
from mro.BaseSpiders.base_spiders import BaseMroSpider
from mro.items import UniversalItem



class Martin(BaseMroSpider):
    name = "ustsubaki"
    search_url = 'http://chains.ustsubaki.com/keyword/?&plpver=1004&key=all&keycateg=100&SchType=2&keyword={}'
    path_to_data = 'mro/spiders/csv_data/ustsubaki/U.S.Tsubaki.csv'
    separator = ','
    fields = ['id', 'main_image']
    attributes = ['Specifications', 'Sprocket Diameters', 'Chain Technical Data', 'Locking Bolts']

    def parse_item(self, response):
        if '/item/' in response.url:
            catalog = response.meta['row']
            E = UniversalItem()
            img = None
            if 'defaul' in self.catalog_main_image[catalog] or self.catalog_id[catalog] in self.catalog_main_image[catalog]:
                img = response.xpath('//img[@itemprop="image"]/@src').extract_first()
            E['main_image'] = response.urljoin(img) if img else ''
            for attr in self.attributes:
                print attr
                path = response.xpath('//h3[@data-id="#{}"]/../div/table/tbody/tr'.format(attr))
                temp = ''
                if path:
                    for i in path:
                        first_part = i.xpath('./td[1]/h2/strong/text()').extract_first() or i.xpath('./td[1]/strong/text()').extract_first()
                        temp += first_part + ':' + ' '.join(i.xpath('./td[2]/span/span[2]/span/text()').extract()) + '|'
                E[attr] = temp[:-1] if temp else ''
            E['id'] = self.catalog_id[catalog]
            E['catalog_number'] = catalog
            return E