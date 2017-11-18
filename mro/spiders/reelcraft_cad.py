# -*- coding: utf-8 -*-
import json
import re
import pandas as pd
import scrapy

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
            dxf = self.custom_extractor(response, '//*[@id="Repeater2_ctl00_lblDXF"]/../@href')
            pdf = self.custom_extractor(response, '//*[@id="Repeater2_ctl00_lblPDF"]/../@href')
            igs = self.custom_extractor(response, '//*[@id="Repeater2_ctl00_lblIGS"]/../@href')
