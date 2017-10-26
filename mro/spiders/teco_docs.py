# -*- coding: utf-8 -*-
import re
import scrapy
import pandas
import unicodedata
from csv import DictReader
from datetime import datetime

from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Compose
from scrapy.contrib.spiders import CrawlSpider
from scrapy.contrib.spiders import Rule
from scrapy.selector import HtmlXPathSelector
from mro.items import TecoDocsItem
from scrapy.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from scrapy.linkextractors import LinkExtractor


class TecoDocsCrawl(CrawlSpider):
	name = "teco_docs"
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
			print catalog_number
			return

		if not response.xpath('//div[@class="productsWrapper"]'):
			print 'without docs'
			return

		names = response.xpath('//div[@class="productsWrapper"]//td/a/text()').extract()
		links = response.xpath('//div[@class="productsWrapper"]//td/a/@href').extract()
		names_links = dict(zip(names, links))

		for key, value in names_links.iteritems():

			item = TecoDocsItem()
			item['ids'] = self.catalog_ids[catalog_number]
			item['catalog_number'] = catalog_number
			item['name'] = key
			item['document'] = 'https://buy.tecowestinghouse.com' + value

			yield item
