# -*- coding: utf-8 -*-
import re
import urllib

import pandas as pd
import scrapy

from mro.items import MartinAttributesItem

out = pd.read_csv("spiders/csv_data/Fennerdrives/Fenner_Drives_additional_descr.csv", sep=';')
catalog = [str(item).strip() for item in list(out.catalog_number)]
ids = list(out.id)
catalog_ids = dict(zip(catalog, ids))
add_descr = list(out.add_descr)
catalog_add_descr = {k:v for k,v in dict(zip(catalog, add_descr)).items() if str(v) == 'nan'}


class Weg(scrapy.Spider):
    name = "fennerdrives"

    def start_requests(self):
        for row in catalog_add_descr.keys():
            url = 'http://www.fennerdrives.com/search/?q=' + row
            yield scrapy.Request(url=url, 
                callback=self.parse_item, 
                meta={'row': row},
                dont_filter=True)


    def parse_item(self, response):
        row = response.meta['row']
        if response.url != 'http://www.fennerdrives.com/search/?q=' + row:
            '''
            attr = ''
            for item in response.xpath('//ul[@class="attributelist"]/li'):
                attr += item.xpath('./strong/text()').extract_first() + item.xpath('./text()').extract()[1].strip() + '|'
            '''
            item = MartinAttributesItem()
            item['ids'] = catalog_ids[row]
            item['catalog_number'] = row
            #item['attributes'] = attr[:-1]
            item['attributes'] = response.xpath('//*[@id="ctl00_ctl00_ctl00_BodyContent_BodyContent_BodyContent_ctl00_pdbiProductDetailBasicInformation_pnlBriefDescription"]/text()').extract_first().strip() or ''
            return item
