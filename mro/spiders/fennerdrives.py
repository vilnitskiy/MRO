# -*- coding: utf-8 -*-
import re
import urllib

import pandas as pd
import scrapy

from mro.items import UniversalItem

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
            item = UniversalItem()
            item['ids'] = catalog_ids[row]
            item['catalog_number'] = row
            #item['attributes'] = attr[:-1]
            item['attributes'] = response.xpath('//*[@id="ctl00_ctl00_ctl00_BodyContent_BodyContent_BodyContent_ctl00_pdbiProductDetailBasicInformation_pnlBriefDescription"]/text()').extract_first().strip() or ''
            return item
'''

class Fennerdrives(scrapy.Spider):
    name = "fennerdrives"
    allowed_domains = ["fennerdrives.com", ]
    data = pd.read_csv("spiders/csv_data/Fennerdrives/Fenner_Drives_images.csv", sep=';')
    catalog_number = list(data.catalog_number)
    main_image = list(data.main_image)
    images = dict(zip(catalog_number, main_image))
    ids = dict(zip(catalog_number, list(data.id)))

    def start_requests(self):
        for catalog_number in self.catalog_number:
            if 'default' in self.images[catalog_number]:
                yield scrapy.Request(
                                url='http://www.fennerdrives.com/search/?q={0}'.format(catalog_number), 
                                callback=self.wrapper(catalog_number)
                            )

    def wrapper(self, catalog_number):
        def parse_item(response):
            # description = response.xpath('//div[@class="description"]/text()').extract_first()
            # description = description.replace('\r\n\t\r\n        ', '').replace('\r\n    \r\n', '')
            main_image = response.xpath('//div[@class="media wl-cf"]/div[@class="primary wl-cf"]/a/@href').extract_first()
            if main_image:
                if self.images.get(catalog_number) and 'default' in self.images[catalog_number]:
                    item = FannerdrivesItem()
                    item['images'] = main_image
                    item['catalog_number'] = catalog_number
                    item['ids'] = self.ids[catalog_number]
                    return item
        return parse_item
'''