# -*- coding: utf-8 -*-
import pandas as pd
import scrapy
import yaml
from scrapy.http import FormRequest

from mro.items import UniversalItem

out = pd.read_csv("mro/spiders/csv_data/Baldor/baldor1.csv", sep=',')
catalog = list(out.catalog_number)
ids = list(out.id)
catalog_ids = dict(zip(catalog, ids))


class Dixon(scrapy.Spider):
    name = "baldor3"

    def start_requests(self):
        for row in out['catalog_number']:
            url = 'https://www.baldorvip.com/Product/Detail/' + row
            yield self.request(url, row)

    def request(self, url, row):
        callback = lambda response: self.parse_item(response, row)
        return scrapy.Request(url=url, callback=callback)

    def parse_item(self, response, row):
        form_data = response.xpath('//*').re(r'\)\.load\("/Product/LoadDrawingsTab", {(.+)}')[0]
        form_data = yaml.load("{" + str(form_data) + "}")
        callback = lambda response: self.parse_item1(response, row)
        return FormRequest(url="https://www.baldorvip.com/Product/LoadDrawingsTab",
                           formdata=form_data,
                           callback=callback)

    def parse_item1(self, response, row):
        index = 0
        for head in response.xpath('//*[@class="drawingHeader"]'):
            item = UniversalItem()
            item['ids'] = catalog_ids[row]
            item['catalog_number'] = row
            item['name'] = head.xpath('text()').extract_first()
            item['url'] = 'https://www.baldorvip.com' + response.xpath('//*[@class="drawing"]/a/@href')[
                index].extract().replace('&amp;', '&')
            index += 1
            yield item
