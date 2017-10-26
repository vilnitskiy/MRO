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
from mro.items import RingspanncorpItem
from scrapy.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from scrapy.linkextractors import LinkExtractor


class RingspanncorpSpider(CrawlSpider):
    name = "ringspanncorp"
    allowed_domains = ["ringspanncorp.com"]
    items = []

    start_urls = ['http://www.ringspanncorp.com/en/products/overview']

    rules = (
        Rule(
            SgmlLinkExtractor(),
            callback='parse_lol',
            follow=True
        ),
    )

    def parse_lol(self, response):
    	if response.xpath('//div[@id="product-view"]'):
    		return self.parse_product(response)

    def parse_product(self, response):
    	hxs = HtmlXPathSelector(response)
    	
    	data = pandas.read_csv("spiders/csv_data/Ringspanncorp/ringspanncorp.csv", sep=',')
    	catalog = list(data.catalog_number)
    	ids = list(data.id)
    	description = list(data.description)
    	key1 = list(data.key1)
    	key2 = list(data.key2)

    	catalog_key1 = dict(zip(catalog, key1))
    	catalog_key2 = dict(zip(catalog, key2))
    	catalog_description = dict(zip(catalog, description))
    	catalog_id = dict(zip(catalog, ids))

    	key1_ids = dict(zip(key1, ids))
    	key2_ids = dict(zip(key2, ids))
    	key1_catalog = dict(zip(key1, catalog))
    	key2_catalog = dict(zip(key2, catalog))
    	key1_description = dict(zip(key1, description))
    	key2_description = dict(zip(key2, description))

    	for catalog_n in catalog:
    		key = catalog_key1[catalog_n]
    		name = ' ' + str(key)
    		if name in response.xpath('//h1').extract_first():
    			if catalog_n not in self.items:
    				item = ToshibaItem()
    				item['ids'] = catalog_id[catalog_n]
    				item['catalog_number'] = catalog_n
    				key_digits = catalog_key1[catalog_n].re('(\d+)')
    				self.items.append(catalog_n)
    				url = response.xpath('//a[@class="cad link_grey"]/@href')
    				yield Request(url=url, meta={'item': item, 'key': key_digits}, callback='cad_page')

    	for catalog_n in catalog:
    		key = catalog_key2[catalog_n]
    		name = ' ' + str(key)
    		name2 = str(key) + ' '
    		if name in response.xpath('//h1').extract_first() or name2 in response.xpath('//h1').extract_first():
    			if catalog_n not in self.items:
    				item = ToshibaItem()
    				item['ids'] = catalog_id[catalog_n]
    				item['catalog_number'] = catalog_n
    				key_digits = catalog_key1[catalog_n].re('(\d+)')
    				self.items.append(catalog_n)
    				url = response.xpath('//a[@class="cad link_grey"]/@href')
    				yield Request(url=url, meta={'item': item, 'key': key_digits}, callback='cad_page')

    def cad_page(self, response):
    	item = response.meta['item']
    	key_digits = response.meta['key_digits']
    	data = pandas.read_csv("spiders/csv_data/Ringspanncorp/ringspanncorp.csv", sep=',')
    	catalog = list(data.catalog_number)
    	ids = list(data.id)
    	description = list(data.description)
    	key1 = list(data.key1)
    	key2 = list(data.key2)

    	catalog_key1 = dict(zip(catalog, key1))
    	catalog_key2 = dict(zip(catalog, key2))
    	catalog_description = dict(zip(catalog, description))
    	catalog_id = dict(zip(catalog, ids))

    	key1_ids = dict(zip(key1, ids))
    	key2_ids = dict(zip(key2, ids))
    	key1_catalog = dict(zip(key1, catalog))
    	key2_catalog = dict(zip(key2, catalog))
    	key1_description = dict(zip(key1, description))
    	key2_description = dict(zip(key2, description))

    	for catalog_n in catalog:
    		key = catalog_key1[catalog_n]
    		name = ' ' + str(key)
    		if name in response.xpath('//h1').extract_first():
    			if catalog_n not in self.items:
    				item = RingspanncorpItem()
    				item['ids'] = catalog_id[catalog_n]
    				item['catalog_number'] = catalog_n
    				self.items.append(catalog_n)
    				url = response.xpath('//a[@class="cad link_grey"]/@href')
    				yield Request(url=url, callback='request_cad')


    	for catalog_n in catalog:
    		key = catalog_key2[catalog_n]
    		name = ' ' + str(key)
    		name2 = str(key) + ' '
    		if name in response.xpath('//h1').extract_first() or name2 in response.xpath('//h1').extract_first():
    			if catalog_n not in self.items:
    				item = RingspanncorpItem()
    				item['ids'] = catalog_id[catalog_n]
    				item['catalog_number'] = catalog_n
    				self.items.append(catalog_n)
    				url = response.xpath('//a[@class="cad link_grey"]/@href')
    				yield Request(url=url, callback='request_cad')



