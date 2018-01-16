# -*- coding: utf-8 -*-
import re
import urllib

import pandas as pd
import scrapy
from mro.items import UniversalItem

out = pd.read_csv("mro/spiders/csv_data/Redlion/red_lion.csv", sep=';')
catalog = [str(item).strip() for item in list(out.catalog_number)]
ids = list(out.id)
catalog_ids = dict(zip(catalog, ids))
img_url = list(out.img_url)
add_descr = list(out.add_descr)
catalog_img_url = {k:v for k,v in dict(zip(catalog, img_url)).items() if (str(catalog_ids[k]) in v) or ('default' in v)}
catalog_add_descr = [k for k,v in dict(zip(catalog, add_descr)).items() if str(v) == 'nan']

class Weg(scrapy.Spider):
    name = "redlion"

    def start_requests(self):
        for row in catalog:
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
            #spec = response.xpath('//section[@class="field field-name-field-specifications field-type-text-with-summary field-label-above view-mode-full"]').extract_first()
            #if spec:
            bruchures = response.xpath('//*[@id="sdownloads"]/div/ul[3]/li')
            if bruchures:
            	item = UniversalItem()
                item['id'] = catalog_ids[row]
                item['catalog_number'] = row
            	for i in bruchures:
            		item['name'] = i.xpath('./a/text()').extract_first() or ''
            		item['url'] = response.urljoin(i.xpath('./a/@href').extract_first())
	                #item['img_url'] = img.split('?')[0]
	                yield item


