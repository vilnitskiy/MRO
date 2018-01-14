# -*- coding: utf-8 -*-
import pandas as pd
import scrapy
from scrapy.http import FormRequest

from mro.items import UniversalItem

out = pd.read_csv("spiders/csv_data/Baldor/baldor1.csv", sep=',')
catalog = list(out.catalog_number)
ids = list(out.id)
catalog_ids = dict(zip(catalog, ids))


class Dixon(scrapy.Spider):
    name = "baldor1"

    def start_requests(self):
        for row in out['catalog_number']:
            url = 'https://www.baldorvip.com/Product/Detail/' + row
            yield self.request(url, row)

    def request(self, url, row):
        callback = lambda response: self.parse_item(response, row)
        return scrapy.Request(url=url, callback=callback)

    def parse_item(self, response, row):
        overview = str(response.xpath('//*[@class="verticalTable"]/tbody').extract_first())
        descr = response.xpath('//*[@id="siteRightColumnContentContainer"]/div[2]/div[2]/text()').extract_first()
        callback = lambda response: self.parse_item1(response, row, overview, descr)
        return FormRequest(url="https://www.baldorvip.com/Product/LoadSpecsTab",
                           formdata={'MaterialNumber': row},
                           callback=callback)

    def parse_item1(self, response, row, overview, descr):
        specs = str(response.xpath('//*').extract_first().encode('ascii', 'ignore'))
        overwiew_specs = specs if specs != '<html></html>' else overview
        item = UniversalItem()
        item['ids'] = catalog_ids[row]
        item['catalog_number'] = row
        item['specs_or_overview'] = overwiew_specs
        item['description'] = descr
        return item
