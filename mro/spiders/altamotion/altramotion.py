# -*- coding: utf-8 -*-
import json
import re

import pandas
import scrapy
from scrapy.contrib.spiders import CrawlSpider

from mro.items import UniversalItem

data = pandas.read_csv("mro/spiders/csv_data/Altamotion/altramotion_with_brands.csv", sep=';')
catalog = list(data.catalog_number)
ids = list(data.id)
descriptions = list(data.description)
images = list(data.img_url)
additional_descriptions = list(data.add_descr)
attributes = list(data.attributes)
brands = list(data.brand)

catalog_ids = dict(zip(catalog, ids))
catalog_descriptions = dict(zip(catalog, descriptions))
catalog_images = dict(zip(catalog, images))
catalog_add_descriptions = dict(zip(catalog, additional_descriptions))
catalog_attributes = dict(zip(catalog, attributes))
catalog_brands = dict(zip(catalog, brands))

brand_key = {
    'Warner Electric': 'warnerelectric',
    'Formsprag': 'formspragclutch',
    'Boston Gear': 'bostongear',
    'HUCO Products': 'huco'
}

class BostongearCrawl(CrawlSpider):
    name = "altramotion"

    allowed_domains = ["product-config.net"]

    start_urls = []

    def start_requests(self):
        for row in catalog:
            url = 'https://www.product-config.net/catalog3/service?unit=english&d=altra.{}&o=product&id={}'.format(
                brand_key[catalog_brands[row]], row)
            yield scrapy.Request(
                url=url,
                callback=self.parse_search,
                dont_filter=True,
                meta={'row': row}
            )

    def parse_search(self, response):
        row = response.meta['row']
        data = json.loads(response.body)
        if data.get('error'):
            return
        add_descr = data.get('longDescription', '')\
                    if str(catalog_add_descriptions[row]) == 'nan'\
                    else catalog_add_descriptions[row]
        image = catalog_images[row]
        if 'dafault' in image or str(catalog_ids[row]) in image:
            image = ('https:' + data.get('imageURL')) if data.get('imageURL') else catalog_images[row]
        attr = catalog_attributes[row]
        if str(attr) == "nan":
            attr = ''          
            attributes = data.get('attributes')
            values = data.get('attributeValues')
            if attributes and values:
                for i, item in enumerate(attributes):
                    if item['dataType'] != 'attachment' and item['dataType'] != 'image' and item['visible']:
                        attr += item['label'] + ':' + values[i] + '|'
                attr = attr[:-1]
        item = UniversalItem()
        item['ids'] = catalog_ids[row]
        item['catalog_number'] = row
        item['description'] = catalog_descriptions[row]
        item['additional_description'] = add_descr
        item['main_image'] = image
        item['attributes'] = attr
        item['brand'] = catalog_brands[row]
        return item




