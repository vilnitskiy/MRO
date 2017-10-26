# -*- coding: utf-8 -*-
import pandas
import scrapy
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector

from mro.items import StatesItem

proxy = pandas.read_csv("spiders/csv_data/States/proxy.csv", sep=',')
proxy_list = list(proxy.proxy)


class StatesSpider(CrawlSpider):
    name = "states"
    allowed_domains = ["statesupply.com"]
    data = pandas.read_csv("spiders/csv_data/States/BellGossett.csv", sep=',')
    catalog = list(data.catalog_number)
    items = []
    index = 0

    def get_proxy(self):
        self.index = self.index + 1 if change else self.index
        if self.index == 100:
            self.index = 0
        return proxy_list[self.index]

    # create list of urls from file
    urls = []
    for sku in catalog:
        urls.append('https://www.statesupply.com/catalogsearch/result/?q=' + str(sku))

    start_urls = urls

    def modify_start_request(self, request):
        proxy = self.get_proxy()
        request.meta['proxy'] = proxy
        return request

    def parse(self, response):
        if response.xpath(
                '//article[@itemtype="http://schema.org/Product"]//h1[@itemprop="name"]/a[@itemprop="url"]/@href'):
            url = response.xpath(
                '//article[@itemtype="http://schema.org/Product"]//h1[@itemprop="name"]/a[@itemprop="url"]/@href').extract()[
                0]
            print url
            return scrapy.Request(url=url, callback=self.parse_product, meta={'proxy': proxy})

    def parse_product(self, response):
        hxs = HtmlXPathSelector(response)

        data = pandas.read_csv("spiders/csv_data/States/BellGossett.csv", sep=',')
        catalog = list(data.catalog_number)
        ids = list(data.id)

        catalog_ids = dict(zip(catalog, ids))

        mpn = response.xpath('//span[@id="mpn"]/text()').extract()[0]
        print mpn
        if mpn in catalog:
            item = StatesItem()
            item['ids'] = catalog_ids[mpn]
            item['description'] = response.xpath('//div[@itemprop="description"]').extract()[0]
            item['catalog_number'] = mpn
            return item
