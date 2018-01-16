# -*- coding: utf-8 -*-
import json

import pandas as pd
import scrapy
from mro.items import UniversalItem

out = pd.read_csv("mro/spiders/csv_data/Rexnord/Rexnord_images.csv", sep=',')
catalog = [str(item).strip() for item in list(out.catalog_number)]
ids = list(out.id)
catalog_ids = dict(zip(catalog, ids))


class RexnordAttrCrawl(scrapy.Spider):
    name = "rexnord_attr"

    def start_requests(self):
        for row in catalog:
            url = 'https://www.rexnord.com/Product/' + row
            yield scrapy.Request(url=url,
                                 callback=self.parse_item,
                                 dont_filter=True,
                                 meta={'row': row}
                                 )

    def create_item(self, row, attributes):
        item = UniversalItem()
        item['ids'] = catalog_ids[row]
        item['catalog_number'] = row
        item['attributes'] = attributes
        return item

    def custom_extractor(self, response, expression):
        data = response.xpath(expression).extract_first()
        return data if data else ''

    def construct_table(self, upc, material, brand, model, descr, htmlContent):
        table = '<table><tr><td>UPC:</td><td>' + upc + '</td></tr><tr><td>Material:</td><td>' + material + '</td></tr><tr><td>Brand:</td><td>' + brand + '</td></tr><tr><td>Model:</td><td>' + model + '</td></tr></table><strong>' + descr + '</strong><p>' + htmlContent
        return table

    def parse_item(self, response):
        row = response.meta['row']
        productId = response.xpath('//*').re(r'"productId":"(.+)","productName')[0]
        model = response.xpath('//*').re(r'name":"(.+)","shortDescription"')[0]
        return scrapy.Request(
            url='https://www.rexnord.com/api/v1/products/' + productId + '?expand=documents,specifications,styledproducts,htmlcontent,attributes,crosssells,relatedproductbrand,excludeconfiguredproduct',
            callback=self.parse_img,
            meta={'row': row, 'model': model}
        )

    def parse_img(self, response):
        row = response.meta['row']
        model = response.meta['model']
        data = response.body_as_unicode()
        data = json.loads(data)
        '''
        img = data['product']['largeImagePath']
        img = img if 'NotFound' not in img else ''
        upc = data['product']['upcCode']
        material = data['product']['modelNumber']
        brand = data['product']['manufacturerItem']
        shortDescription = data['product']['shortDescription']
        htmlContent = data['product']['htmlContent']

        descr = self.construct_table(upc, material, brand, model, shortDescription, htmlContent)
        '''
        attributes = ''
        list_attr = data['product']['attributeTypes']
        if list_attr != []:
            for item in list_attr:
                attributes = attributes + item['name'] + ':' + item['attributeValues'][0]['valueDisplay'] + '|'
            attributes = attributes[:-1]

        return self.create_item(row, attributes)
