# -*- coding: utf-8 -*-
import json
import re
import pandas as pd
import scrapy
import lxml.html
import lxml.html.clean as clean
from mro.items import UniversalItem

out = pd.read_csv("spiders/csv_data/Reelcraft/Export_for_products_product.csv", sep=',')
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
    name = "reelcraft"

    def start_requests(self):
        for row in catalog:
            url = 'https://www.reelcraft.com/catalog/product_search.aspx?Search={}&category=default'.format(row)
            yield scrapy.Request(url=url,
                                 callback=self.parse_item,
                                 dont_filter=True,
                                 meta={'row': row, 'proxy': '37.48.118.90:13040'}
                                 )


    def custom_extractor(self, response, expression):
        data = response.xpath(expression).extract_first()
        return data if data else ''

    @staticmethod
    def remove_html_attributes(string):
        html = lxml.html.fromstring(string)
        safe_attrs = clean.defs.safe_attrs
        cleaner = clean.Cleaner(safe_attrs_only=True, safe_attrs=frozenset())
        cleansed = cleaner.clean_html(html)
        string = lxml.html.tostring(cleansed)
        return re.sub(r'&#\d+;', '', string)

    def parse_item(self, response):
        row = response.meta['row']
        if 'No search results found' not in response.body_as_unicode():
            if ('default' in catalog_images[row]) or (str(catalog_ids[row]) in catalog_images[row]):
                img = response.xpath('//img[@alt="Reel Image"]/@src').extract_first()
                img = img if (img != None) and ('not_available' not in img) else catalog_images[row]
            else:
                img = catalog_images[row]
            if str(catalog_additional_description[row]) == 'nan':
                add_descr = self.remove_html_attributes(response.xpath('//table[1]').extract()[1])
                next_content = self.custom_extractor(response, '//ul[@class="bullets"]')
                add_descr += next_content
            else:
                add_descr = catalog_additional_description[row]
            if str(catalog_attributes[row]) == 'nan':
                table = self.custom_extractor(response, '//b[text()="Part Number"]/../../../..').encode('utf-8')
                table = self.remove_html_attributes(table)
                table = table.replace('\n', '').replace('\t', '').replace('  ', '')
                attr = table
            else:
                attr = catalog_attributes[row]
            item = UniversalItem()
            item['ids'] = catalog_ids[row]
            item['catalog_number'] = row
            item['description'] = catalog_description[row]
            item['main_image'] = img
            item['additional_description'] = add_descr
            item['attributes'] = attr
            return item
