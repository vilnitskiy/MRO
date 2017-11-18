# -*- coding: utf-8 -*-
import json
import re
import pandas as pd
import scrapy

from mro.items import MartinItem

out = pd.read_csv("spiders/csv_data/Martin/martin_catalog.csv", sep=',')
catalog = [str(item).strip() for item in list(out.catalog_number)]
ids = list(out.id)
description = list(out.description)
images = list(out.main_image)
additional_description = list(out.additional_description)
attributes = list(out.attributes)
catalog_ids = dict(zip(catalog, ids))
catalog_images = dict(zip(catalog, images))
catalog_description = dict(zip(catalog, description))
catalog_additional_description = dict(zip(catalog, additional_description))
catalog_attributes = dict(zip(catalog, attributes))


class Martin(scrapy.Spider):
    name = "martin"

    def start_requests(self):
        for row in catalog:
            url = 'http://productcatalog.martinsprocket.com/views/productinfo.aspx?Part_Number=' + row
            yield scrapy.Request(url=url,
                                 callback=self.parse_item,
                                 dont_filter=True,
                                 meta={'row': row}
                                 )


    def custom_extractor(self, response, expression):
        data = response.xpath(expression).extract_first()
        return data if data else ''

    def parse_item(self, response):
        row = response.meta['row']
        if ('default' in catalog_images[row]) or (str(catalog_ids[row]) in catalog_images[row]):
            img = response.xpath('//*[@id="main"]/div[2]/div[1]/div[1]/img/@src').extract_first()
            img = response.urljoin(img) if img != None else catalog_images[row]
        else:
            img = catalog_images[row]
        if str(catalog_additional_description[row]) == 'nan':
            add_descr = self.custom_extractor(response, '//*[@id="main"]/div[2]/div[1]/div[2]/div[2]/text()')
        else:
            add_descr = catalog_additional_description[row]
        if str(catalog_attributes[row]) == 'nan':
            table = self.custom_extractor(response, '//*[@id="tabs-00001"]/table').encode('utf-8')
            table = re.sub(r'<table .+>', '<table>', table)
            table = re.sub(r'<td .+>', '<td>', table)
            table = table.replace(' ', '')
            table = table.replace('</td>\r\r<td>', '</td></tr><tr><td>')
            table = table.replace('</td>\n\n<td>', '</td></tr><tr><td>')
            table = table.replace('</td>\r\n\r\n<td>', '</td></tr><tr><td>')
            table = table.replace('\r', '')
            table = table.replace('\n', '')
            attr = table
        else:
            attr = catalog_attributes[row]
        item = MartinItem()
        item['ids'] = catalog_ids[row]
        item['catalog_number'] = row
        item['description'] = catalog_description[row]
        item['main_image'] = img
        item['additional_description'] = add_descr
        item['attributes'] = attr
        return item
