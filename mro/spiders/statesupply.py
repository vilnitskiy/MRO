# -*- coding: utf-8 -*-
import pandas as pd
import scrapy
import urllib
from mro.items import PatriotItem
 

out = pd.read_csv("spiders/csv_data/statesupply/patriot.csv", sep=',')
catalog = list(out.catalog_number)
ids = list(out.id)
catalog_ids = dict(zip(catalog, ids))

proxy = pd.read_csv("spiders/csv_data/statesupply/proxy.csv", sep=',')
proxy_list = list(proxy.proxy)

class Statesupply(scrapy.Spider):
    name = "statesupply"
    index = 0

    def get_proxy(self, change=0):
        self.index = self.index + 1 if change else self.index
        try:
            proxy = proxy_list[self.index]
        except Exception:
            raise CloseSpider('empty poxy list')
        else:
            return proxy

    def start_requests(self):
        for row in out['catalog_number']:
            proxy = self.get_proxy()
            yield self.request(row, proxy)

    def request(self, row, proxy):
        url = 'https://www.statesupply.com/catalogsearch/result/?q=' + urllib.quote_plus(str(row).strip())
        errback = lambda failure: self.repeat(row)
        return scrapy.Request(url=url, 
                              callback=self.parse_item1,
                              errback=errback,
                              meta={'meta_row': row, 'proxy': proxy, 'download_timeout': 20},
                              dont_filter=True
                              )

    def repeat(self, row):
        proxy = self.get_proxy(1)
        return self.request(row, proxy)

    def create_item(self, meta_row, overview=''):
        item = PatriotItem()
        item['ids'] = catalog_ids[meta_row]
        item['catalog_number'] = str(meta_row).strip()
        item['descr'] = overview
        return item

    def parse_item1(self, response):
        url = response.xpath('//*[@id="product-list"]/article[1]/div/div/header/h1/a/@href').extract_first()
        if url:
            errback = lambda failure: self.repeat(response.meta['meta_row'])
            proxy = self.get_proxy()
            return scrapy.Request(url=url,
                                  errback=errback,
                                  callback=self.parse_item2,
                                  meta={'meta_row': response.meta['meta_row'], 'proxy': proxy, 'download_timeout': 20},
                                  dont_filter=True
                                  )
        else:
            return self.create_item(response.meta['meta_row'])

    def parse_item2(self, response):
        meta_row = response.meta['meta_row']
        if str(meta_row).strip().lower() == response.xpath('//*[@id="mpn"]/text()').extract_first().lower():
            overview = response.xpath('//*[@id="overview"]/div/div/div/p').extract_first()
            return self.create_item(meta_row, overview)
        else:
            return self.create_item(meta_row)





