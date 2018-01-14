# -*- coding: utf-8 -*-
import pandas as pd
import scrapy

from mro.items import UniversalItem

out = pd.read_csv("spiders/csv_data/Rexnord/Product_images.csv", sep=',')
catalog = [str(item).strip() for item in list(out.catalog_number)]
ids = list(out.id)
catalog_ids = dict(zip(catalog, ids))


class Mcr(scrapy.Spider):
    name = "rexnord_cads_items"
    allowed_domains = ["rexnord.com"]

    def start_requests(self):
        for row in catalog:
            url = 'https://www.rexnord.com/Product/' + row
            yield scrapy.Request(url=url,
                                 callback=self.parse_item,
                                 dont_filter=True,
                                 meta={'row': row})

    def parse_item(self, response):
        row = response.meta['row']
        cadid = response.xpath('//script[contains(text(), "insite.catalog.catalogPageGlobal")]').re(r'"cadid":(.+?),')
        if cadid:
            if cadid[0] != '""':
                item = UniversalItem()
                item['ids'] = catalog_ids[row]
                item['catalog_number'] = row
                item['cadid'] = cadid[0]
                return item
