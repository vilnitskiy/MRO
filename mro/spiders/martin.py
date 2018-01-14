# -*- coding: utf-8 -*-
import json
import re
import pandas as pd
import scrapy
from mro.BaseSpiders.base_spiders import BaseMroSpider



class Martin(BaseMroSpider):
    name = "martin"
    search_url = 'http://productcatalog.martinsprocket.com/views/productinfo.aspx?Part_Number={}'
    path_to_data = 'spiders/csv_data/Martin/martin_catalog.csv'
    separator = ','
    fields = ['id', 'main_image', 'additional_description', 'attributes', 'description']


    def custom_extractor(self, response, expression):
        data = response.xpath(expression).extract_first()
        return data if data else ''

    def parse_item(self, response):
        row = response.meta['row']
        if ('default' in self.catalog_main_image[row]) or (str(self.catalog_id[row]) in self.catalog_main_image[row]):
            img = response.xpath('//*[@id="main"]/div[2]/div[1]/div[1]/img/@src').extract_first()
            img = response.urljoin(img) if img != None else self.catalog_main_image[row]
        else:
            img = self.catalog_main_image[row]
        if str(self.catalog_additional_description[row]) == 'nan':
            add_descr = self.custom_extractor(response, '//*[@id="main"]/div[2]/div[1]/div[2]/div[2]/text()')
        else:
            add_descr = self.catalog_additional_description[row]
        if str(self.catalog_attributes[row]) == 'nan':
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
            attr = self.catalog_attributes[row]
        return {
            'id': self.catalog_id[row],
            'catalog_number': row,
            'description': self.catalog_description[row],
            'main_image': img,
            'additional_description': add_descr,
            'attributes': attr
        }
