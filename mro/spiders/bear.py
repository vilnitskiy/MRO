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
from mro.items import BearImgItem
from scrapy.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from scrapy.linkextractors import LinkExtractor


class BearSpider(CrawlSpider):
	name = "bear"
	allowed_domains = ["http://bearingfinder.ntnamericas.com"]
	pr = False
	data = pandas.read_csv("spiders/csv_data/Bearingfinder/NTN.csv", sep=',')
	catalog = list(data.catalog_number)
	ids = list(data.id)
	catalog_ids = dict(zip(catalog, ids))
	
	# create list of urls from file
	urls = []
	for sku in catalog:
		urls.append('http://bearingfinder.ntnamericas.com/keyword/?keyword={}&refer=http://bearingfinder.ntnamericas.com'.format(str(sku)))
	start_urls = urls

	def parse(self, response):
		if response.xpath('//nav[@id="plp-product-title"]').extract():
			return self.parse_product(response)

	def parse_product(self, response):
		hxs = HtmlXPathSelector(response)

		row = str(response.xpath('//nav[@id="plp-product-title"]/h1/text()').extract()[0])
		catalog_number = re.search("# (.+),", row).group(1)
		if ', ' in catalog_number:
			catalog_number = catalog_number.split(',', 1)[0]

		item = BearImgItem()
		item['ids'] = self.catalog_ids[catalog_number]
		item['catalog_number'] = catalog_number
		item['main_image'] = 'http://bearingfinder.ntnamericas.com' + str(response.xpath('//ul[@class="ad-thumb-list"]//img/@src').extract()[0]).replace('ImgSmall', 'Asset')
		descr = response.xpath('//a[@name="Technical Specifications"]/..').extract()[0]
		descr1 = response.xpath('//a[@name="Dimensional Specifications"]/..').extract()[0]
		item['additional_descriptions'] = descr + descr1

		return item
