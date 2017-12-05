# -*- coding: utf-8 -*-
import re
import urllib

import pandas as pd
import scrapy

from mro.items import UnivarsalItem

out = pd.read_csv("spiders/csv_data/Redlion/red_lion.csv", sep=';')
catalog = [str(item).strip() for item in list(out.catalog_number)]
ids = list(out.id)
catalog_ids = dict(zip(catalog, ids))
img_url = list(out.img_url)
catalog_img_url = {k:v for k,v in dict(zip(catalog, img_url)).items() if (str(catalog_ids[k]) in v) or ('default' in v)}


class Weg(scrapy.Spider):
    name = "redlion"

    def start_requests(self):
        for row in catalog_img_url.keys():
            url = 'http://www.redlion.net/search/node/' + row
            yield scrapy.Request(url=url, 
                callback=self.parse_item, 
                meta={'row': row},
                dont_filter=True)


    def parse_item(self, response):
        row = response.meta['row']
        url = response.xpath('//ol[@class="search-results node-results"]/li[1]/h3/a/@href').extract_first()
        if url:
            return scrapy.Request(url=url, 
                callback=self.parse_item2, 
                meta={'row': row},
                dont_filter=True)

    def parse_item2(self, response):
        row = response.meta['row']
        if row in (response.xpath('//*[@class="field field-name-field-model field-type-text field-label-above view-mode-full"]').extract_first() or ''):
            img = response.xpath('//div[@class="main-product-image"]/a/@href').extract_first()
            if img:
                item = UnivarsalItem()
                item['id'] = catalog_ids[row]
                item['catalog_number'] = row
                item['img_url'] = img.split('?')[0]
                return item


