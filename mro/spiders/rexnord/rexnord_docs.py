# -*- coding: utf-8 -*-
import json

import pandas as pd
import scrapy

from mro.items import UniversalItem

out = pd.read_csv("mro/spiders/csv_data/Rexnord/Rexnord_images.csv", sep=',')
catalog = [str(item).strip() for item in list(out.catalog_number)]
ids = list(out.id)
catalog_ids = dict(zip(catalog, ids))


class RexnordImagesCrawl(scrapy.Spider):
    name = "rexnord_docs"

    def start_requests(self):
        for row in catalog:
            url = 'https://www.rexnord.com/Product/' + row
            yield scrapy.Request(url=url,
                                 callback=self.parse_item,
                                 dont_filter=True,
                                 meta={'row': row}
                                 )

    def create_item(self, row, name, url):
        item = UniversalItem()
        item['ids'] = catalog_ids[row]
        item['catalog_number'] = row
        item['name'] = name
        item['url'] = url
        return item

    def custom_extractor(self, response, expression):
        data = response.xpath(expression).extract_first()
        return data if data else ''

    def parse_item(self, response):
        row = response.meta['row']
        productId = response.xpath('//*').re(r'"productId":"(.+)","productName')[0]
        return scrapy.Request(
            url='https://www.rexnord.com/api/v1/products/' + productId + '?expand=documents,specifications,styledproducts,htmlcontent,attributes,crosssells,relatedproductbrand,excludeconfiguredproduct',
            callback=self.parse_img,
            meta={'row': row}
        )

    def parse_img(self, response):
        row = response.meta['row']
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
        list_docs = data['product']['documents']
        if list_docs != []:
            for item in list_docs:
                url = 'https://www.rexnord.com/api/v2/getProductDocuments?documentNumbers=' + item['filePath']
                yield scrapy.Request(url=url,
                                     callback=self.extract_docs,
                                     dont_filter=True,
                                     meta={'row': row}
                                     )

    def extract_docs(self, response):
        row = response.meta['row']
        data = response.body_as_unicode()
        data = json.loads(data)
        list_docs = data['productDocuments']
        for item in list_docs:
            yield self.create_item(row, item['name'], response.urljoin(item['filePath']))
