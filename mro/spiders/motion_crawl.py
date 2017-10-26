# -*- coding: utf-8 -*-
import re
import scrapy
import pandas
from csv import DictReader
from datetime import datetime
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Compose
from scrapy.contrib.spiders import CrawlSpider
from scrapy.contrib.spiders import Rule
from scrapy.selector import HtmlXPathSelector
from mro.items import MotionItem
from scrapy.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from scrapy.linkextractors import LinkExtractor


class MotionCrawl(CrawlSpider):
    name = "motion"
    allowed_domains = ["motionindustries.com"]
    items = []

    start_urls = ['https://www.motionindustries.com/productCatalogSearch.jsp?q=dodge']

    rules = (
        Rule(
            SgmlLinkExtractor(
                restrict_xpaths=(
                    '//div[@class="taxonomy-node-l1"]//a',
                    '//div[@class="pagination ui-helper-clearfix"]//li'
                ),
            ),
            callback='parse_lol',
            follow=True
        ),
    )

    def parse_lol(self, response):
        if response.xpath('//div[@class="result-item-detail"]'):
            return self.parse_product(response)

    def parse_product(self, response):
        hxs = HtmlXPathSelector(response)

        if not response.xpath('//div[@class="result-item-detail"]//h1[@class="manufacturer-name"]/text()'):
            return
        codes = response.xpath('//div[@class="result-item-detail"]//h1[@class="manufacturer-name"]/text()').re('Dodge \(Baldor\) (.+)')
        mi = response.xpath('//div[@class="result-item-detail"]//div[@class="item-property"]/a/text()').re('# (.+)')

        d = zip(codes, mi)

        for it, l in d:
            if it not in self.items:
                item = MotionItem()
                item['code'] = it
                l = l.replace('\r', '')
                l = l.replace('\n', '')
                item['mi_item'] = l
                self.items.append(it)
                yield item
