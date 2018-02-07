# -*- coding: utf-8 -*-
import json
import re
import pandas as pd
import scrapy
from mro.BaseSpiders.base_spiders import BaseMroSpider
from mro.items import UniversalItem



class Martin(BaseMroSpider):
    name = "remko"
    search_url = 'http://products.remcoproducts.com/Search.aspx?Keyword={}'
    path_to_data = 'mro/spiders/csv_data/remko/Remco Products.csv'
    separator = ','
    exclude_fields = ['description']

    def parse_item(self, response):
        catalog = response.meta['row']
        url = response.xpath('//div[@class="SingleProductDisplaySKU"]/a[text()="{}"]/@href'.format(catalog)).extract_first()
        if url:
            return scrapy.Request(url=url, callback=self.parse_next, meta=response.meta)

    def parse_next(self, response):
        catalog = response.meta['row']
        img = self.catalog_main_image[catalog]
        if 'default' in img or self.catalog_id[catalog] in img:
            img = response.xpath('//*[@id="ucContentMiddleCenter_MainImage"]/@src').extract_first()
            if img:
                img = response.urljoin(img)
        add_descr = self.catalog_additional_description[catalog]
        if str(add_descr) == 'nan':
            add_descr = response.xpath('//*[@id="ucContentMiddleCenter_lblDescription"]/p/text()').extract_first()
        attr = self.catalog_attributes[catalog]
        if str(attr) == 'nan':
            attr = ''
            for li in response.xpath('//*[@id="ucContentMiddleCenter_lstProperties"]/li'):
                try:
                    temp = li.xpath('./span[@class="ProductPropertyLabel"]/text()').extract_first().strip() +\
                    li.xpath('./span[@class="ProductProperty"]/text()').extract_first() + '|'
                except Exception:
                    pass
                else:
                    attr += temp
        return {
            'id': self.catalog_id[catalog],
            'catalog_number': catalog,
            'main_image': img,
            'additional_description': add_descr,
            'attributes': attr[:-1]
        }


