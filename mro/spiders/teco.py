# -*- coding: utf-8 -*-
import pandas
import scrapy
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector

from mro.items import TecoItem


class TecoCrawl(CrawlSpider):
    name = "teco_attr"
    allowed_domains = ["tecowestinghouse.com"]

    data = pandas.read_csv("spiders/csv_data/Teco/teco.csv", sep=',')
    catalog = list(data.catalog_number)
    ids = list(data.id)
    catalog_ids = dict(zip(catalog, ids))

    # create list of urls from file
    urls = []
    for sku in catalog:
        urls.append('https://buy.tecowestinghouse.com/SearchProduct.aspx?product=' + str(sku))
    start_urls = urls

    def parse(self, response):
        if response.xpath('//tr[@class="rgRow"]//a/@href').extract():
            url = 'https://buy.tecowestinghouse.com' + response.xpath('//tr[@class="rgRow"]//a/@href').extract()[0]

            # print response.xpath('//tr[@class="rgRow"]//a/@title').extract()
            catalog_number = response.xpath('//tr[@class="rgRow"]//a/@title').extract()[0]
            return scrapy.Request(
                url=url,
                callback=self.parse_product,
                meta={'sku': catalog_number},
                dont_filter=True
            )

    def parse_product(self, response):
        hxs = HtmlXPathSelector(response)

        # sku = response.url.rsplit('/', 1)[-1]

        catalog_number = response.meta['sku']
        if catalog_number not in self.catalog:
            print '--------'
            print catalog_number
            return

        item = TecoItem()
        item['ids'] = self.catalog_ids[catalog_number]
        item['catalog_number'] = catalog_number

        attr_names = response.xpath('//table[@class="rgMasterTable MotorsDetailPage"]/tbody/tr/td[1]/text()').extract()
        attr_values = response.xpath('//table[@class="rgMasterTable MotorsDetailPage"]/tbody/tr/td[2]/text()').extract()
        attr = dict(zip(attr_names, attr_values))

        for key in attr.keys():
            if str(key) == 'Motor Type' or str(key) == 'Drives Type' or str(key) == 'Approx. Weight' or str(
                    key) == 'List Price' or attr[key] == u'\xa0':
                del attr[key]

        attrs = ""
        for key, value in attr.iteritems():
            attrs += str(key) + ":" + str(value) + "|"
        attrs = attrs[:-1]

        if attrs == "":
            return

        item['attributes'] = attrs

        return item
