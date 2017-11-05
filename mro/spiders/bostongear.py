# -*- coding: utf-8 -*-
import json
import re

import pandas
import scrapy
from scrapy.contrib.spiders import CrawlSpider

from mro.items import BostongearItem

data = pandas.read_csv("spiders/csv_data/Bostongear/boston_gear_data.csv", sep=',')
catalog = list(data.catalog_number)
ids = list(data.id)
codes = list(data.code)
documents = list(data.documents)
additional_descriptions = list(data.additional_description)

catalog_ids = dict(zip(catalog, ids))
catalog_codes = dict(zip(catalog, codes))
catalog_documents = dict(zip(catalog, documents))
catalog_descriptions = dict(zip(catalog, additional_descriptions))


class BostongearCrawl(CrawlSpider):
    name = "bostongear"

    allowed_domains = ["bostongear.com"]

    start_urls = []

    def start_requests(self):
        for row in catalog:
            url = 'http://www.product-config.net/catalog3/service?o=keys&d=altra.bostongear&cdskeys={}&unit=english/'.format(
                row)
            yield scrapy.Request(
                url=url,
                callback=self.parse_search,
                dont_filter=True,
                meta={'row': row}
            )

    def parse_search(self, response):
        row = response.meta['row']
        try:
            products = json.loads(response.body)['products']
        except ValueError:
            return
        if not products:
            if 'code' not in response.meta:
                code = catalog_codes[row]
                if str(code) == 'nan':
                    return
                else:
                    url = 'http://www.product-config.net/catalog3/service?o=keys&d=altra.bostongear&cdskeys={}&unit=english/'.format(
                        code)
                    return scrapy.Request(
                        url=url,
                        meta={'row': row, 'code': code},
                        callback=self.parse_search,
                        dont_filter=True
                    )
            elif str(catalog_descriptions[row]) != 'nan' or str(catalog_documents[row]) != 'nan':
                item = BostongearItem()
                item['ids'] = catalog_ids[row]
                item['catalog_number'] = row
                item['code'] = catalog_codes[row]
                item['image'] = ''
                item['documents'] = catalog_documents[row]
                item['additional_description'] = catalog_descriptions[row]
                return item
        else:
            products = products[0]
            item = BostongearItem()
            item['ids'] = catalog_ids[row]
            item['catalog_number'] = row
            item['code'] = catalog_codes[row]
            item['image'] = 'https:' + str(products['imageURL'])

            if str(catalog_descriptions[row]) == 'nan':
                item['additional_description'] = self.get_descriptions(products)
            else:
                item['additional_description'] = catalog_descriptions[row]

            if str(catalog_documents[row]) == 'nan':
                docs = re.findall("'(http://www\.altraliterature\.com/.+?)'", str(products))
                return self.make_items(item, docs)
            else:
                item['documents'] = catalog_documents[row]
            return item

    def get_descriptions(self, products):
        description = products.get('longDescription', '')
        names_raw = products['attributes']
        values_raw = products['attributeValues']
        attributes = {}

        for index, name in enumerate(names_raw):
            if name['dataType'] == 'attachment':
                break
            if name['label'] != 'Description':
                attributes[name['label']] = values_raw[index]
        specs = '<p>' + description.encode('utf-8') + '</p><br>' + '<table>'
        for row in attributes:
            specs += '<tr><th>{}</th>'.format(row.encode('utf-8')) + '<th>{}</th></tr>'.format(attributes[row].encode('utf-8'))
        specs += '</table>'
        return specs

    def make_items(self, item, docs):
        for doc in docs:
            item['documents'] = doc
            yield item
