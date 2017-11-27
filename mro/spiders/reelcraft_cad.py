# -*- coding: utf-8 -*-
import json
import re
import pandas as pd
import scrapy
from mro.items import MartinCADItem

out = pd.read_csv("spiders/csv_data/Reelcraft/Export_for_products_product.csv", sep=',')
catalog = [str(item).strip() for item in list(out.catalog_number)]
ids = list(out.id)
catalog_ids = dict(zip(catalog, ids))


class Martin(scrapy.Spider):
	name = "reelcraft_cad"

	def start_requests(self):
		for row in catalog:
			url = 'https://www.reelcraft.com/catalog/product_search.aspx?Search={}&category=default'.format(row)
			yield scrapy.Request(url=url,
								 callback=self.parse_item,
								 dont_filter=True,
								 meta={'row': row}
								 )

	@staticmethod
	def custom_extractor(response, expression):
		data = response.xpath(expression).extract_first()
		return data if data else ''

	def parse_item(self, response):
		row = response.meta['row']
		if 'No search results found' not in response.body_as_unicode():
			'''
			dxf = self.custom_extractor(response, '//*[@id="Repeater2_ctl00_lblDXF"]/../@href')
			if dxf:
				yield scrapy.Request(url=dxf,
								 callback=self.download,
								 dont_filter=True,
								 meta={'row': row, 'cad': 'dxf'}
								 )
			
			pdf = self.custom_extractor(response, '//*[@id="Repeater2_ctl00_lblPDF"]/../@href')
			if '.zip' in pdf:
				yield scrapy.Request(url=pdf,
								 callback=self.download,
								 dont_filter=True,
								 meta={'row': row, 'cad': 'pdf'}
								 )
			'''
			igs = self.custom_extractor(response, '//*[@id="Repeater2_ctl00_lblIGS"]/../@href')
			if igs:
				yield scrapy.Request(url=igs,
								 callback=self.download,
								 dont_filter=True,
								 meta={'row': row, 'cad': 'igs'}
								 )

	def download(self, response):
		cad = response.meta['cad']
		row = response.meta['row']
		file_name = response.url.split('/')[-1]
		with open('results/Reelcraft/' + cad + '_cad/' + file_name, 'wb') as file:
			file.write(response.body)
		item = MartinCADItem()
		item['ids'] = catalog_ids[row]
		item['catalog_number'] = row
		item['pdf'] = file_name
		return item