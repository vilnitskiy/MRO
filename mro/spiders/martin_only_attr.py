# -*- coding: utf-8 -*-
import json
import re
import pandas as pd
import scrapy

from mro.items import MartinAttributesItem

out = pd.read_csv("spiders/csv_data/Martin/martin_next.csv", sep=',')
catalog = [str(item).strip() for item in list(out.catalog_number)]
ids = list(out.id)
attributes = list(out.attributes)
catalog_ids = dict(zip(catalog, ids))
catalog_attributes = dict(zip(catalog, attributes))


class Martin(scrapy.Spider):
    name = "martin_attr"

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
        if str(catalog_attributes[row]) == 'nan':
            table = self.custom_extractor(response, '//*[@id="tabs-00001"]/table').encode('utf-8')
            table = re.sub(r'<table .+>', '<table>', table)
            table = re.sub(r'<td .+>', '<td>', table)
            table = table.replace('  ', '')
            table = table.replace('</td>\r\r<td>', '</td></tr><tr><td>')
            table = table.replace('</td>\n\n<td>', '</td></tr><tr><td>')
            table = table.replace('</td>\r\n\r\n<td>', '</td></tr><tr><td>')
            table = table.replace('\r', '')
            table = table.replace('\n', '')
            attr = table
            item = MartinAttributesItem()
            item['ids'] = catalog_ids[row]
            item['catalog_number'] = row
            item['attributes'] = attr
            return item
