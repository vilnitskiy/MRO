# -*- coding: utf-8 -*-
import pandas as pd
import scrapy

from mro.items import UniversalItem

out = pd.read_csv("mro/spiders/csv_data/Dixon/dixon_additional_descr.csv", sep=',')
catalog = list(out.catalog_number)
ids = list(out.id)
catalog_ids = dict(zip(catalog, ids))


class Dixon(scrapy.Spider):
    name = "dixon"

    def start_requests(self):
        for row in out['catalog_number']:
            url = 'https://www.dixonvalve.com/product/' + row
            yield scrapy.Request(url=url, callback=self.parse_item)

    def parse_item(self, response):
        for column in response.xpath('//*[@id="block-dixon-product-product-resources"]/section/div[2]/div/div'):
            i = 1
            for h4 in column.xpath('h4'):
                item = UniversalItem()
                item['ids'] = catalog_ids[
                    response.xpath('//*[@id="product-specs"]/table/tbody/tr[1]/td/text()').extract_first()]
                item['name'] = h4.xpath('text()').extract_first()
                expression = 'div[%s]/div[1]/ul/li' % i
                i += 1
                for li in column.xpath(expression):
                    item['url'] = li.xpath('a/@href').extract_first()
                    yield item
