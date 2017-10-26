# -*- coding: utf-8 -*-
import re

import pandas
import scrapy
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector

from mro.items import McrsafetyItem


class McrsafetyCrawl(CrawlSpider):
    name = "mcrsafety"
    allowed_domains = ["mcrsafety.com"]
    items = []

    data = pandas.read_csv("spiders/csv_data/Mcrsafety/MCR_Safety.csv", sep=',')

    start_urls = []

    for number in list(data.catalog_number):
        start_urls.append('http://www.mcrsafety.com/search?s=' + number)

    def parse(self, response):
        names = response.xpath('//h3[@class="black"]/text()').extract()
        catalog_number = re.search('s=(.+)', response.url).group(1)
        print names
        print catalog_number
        url = ''
        number = ''

        for name in names:
            if name == catalog_number:
                print \
                response.xpath('//h3[@class="black"][contains(text(), "{}")]/../../a/@href'.format(name)).extract()[0]
                url = 'http://www.mcrsafety.com' + response.xpath(
                    '//h3[@class="black"][contains(text(), "{}")]/../../a/@href'.format(name)).extract()[0]
                number = name
                break
        if url == '':
            return
        return scrapy.Request(url=url, meta={'number': number}, callback=self.parse_product)

    def parse_product(self, response):
        hxs = HtmlXPathSelector(response)
        print 'parse'

        data = pandas.read_csv("spiders/csv_data/Mcrsafety/MCR_Safety.csv", sep=',')
        catalog = list(data.catalog_number)
        ids = list(data.id)
        catalog_id = dict(zip(catalog, ids))

        number = response.meta['number']

        item = McrsafetyItem()

        item['ids'] = catalog_id[number]
        item['catalog_number'] = number
        item['image'] = response.xpath('//div[@class="material-image-container"]//img/@src').extract()[0].replace(
            "Download ", "")
        item['document_name'] = response.xpath('//div[@class="material-specsheet"]//a/span/text()').extract()[
            0].replace("Download ", "")
        item['document_url'] = 'http://www.mcrsafety.com' + \
                               response.xpath('//div[@class="material-specsheet"]//a/@href').extract()[0]
        item['additional_description'] = response.xpath('//div[@class="black material-long-description"]').extract()[
                                             0] + \
                                         response.xpath('//div[@class="row material-attr-grouping"]').extract()[0]
        item['features'] = response.xpath('//div[@id="features"]').extract()[0]
        item['specs'] = response.xpath('//div[@id="specs"]').extract()[0]
        item['industry_application'] = response.xpath('//div[@id="industries"]').extract()[0]

        return item
