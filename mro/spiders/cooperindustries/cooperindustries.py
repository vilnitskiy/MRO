# -*- coding: utf-8 -*-
import json
import re
import pandas as pd
import scrapy
from mro.BaseSpiders.base_spiders import BaseMroSpider



class Martin(BaseMroSpider):
    name = "cooperindustries"
    search_url = 'http://search.eaton.com/cgi-bin/query-meta?v%3Aproject=eaton_cooper_industries&query={}'
    path_to_data = 'mro/spiders/csv_data/cooperindustries/Product_2018-3-1 (Cooper Wiring Devices).csv'
    separator = ','
    output_fields = ('id', 'catalog_number', 'img', 'add_descr',  'attributes')

    def parse_item(self, response):
        catalog = response.meta['row']
        if catalog in (response.xpath('//ol[@class="results"]/li[1]').extract_first() or ''):
            url = response.xpath('//a[@class="title"]/@href').extract_first()
            return scrapy.Request(url=response.urljoin(url), 
                callback=self.parse_next, meta=response.meta, dont_filter=True)

    def parse_next(self, response):
        catalog = response.meta['row']
        if catalog.lower() in (response.xpath('//td[text()="Catalog Number"]/../td[2]/text()').extract_first() or '').lower():
            img = response.xpath('//div[contains(@class, "product-image")]/img/@src').extract_first() or ''
            if img:
                img = response.urljoin(img)
            add_descr = response.xpath('//div[contains(@class, "product-details")]/p/text()').extract_first() or ''
            attributes = ''
            table = response.xpath('//table[@summary="Product details"]/tbody/tr')
            if table:
                for tr in table:
                    attributes += tr.xpath('./td[1]/text()').extract_first() + ':' + tr.xpath('./td[2]/text()').extract_first() + '|'
            return self.create_item(self.catalog_id[catalog],
                catalog,
                img,
                add_descr,
                attributes[:-1] if attributes else ''
                )




