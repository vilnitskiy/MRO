# -*- coding: utf-8 -*-
import re
import pandas as pd

import scrapy
from scrapy.contrib.spiders import CrawlSpider
from mro.items import UniversalItem


out = pd.read_csv("spiders/csv_data/Carlisle/Carlisle.csv", error_bad_lines=False, sep=',')
ids = list(out.id)
catalog = list(out.catalog_number)
descriptions = list(out.description)
descriptions_catalog = dict(zip(descriptions, catalog))

catalog_descriptions_fixed = {}
for x in descriptions:
    if str(x) == 'nan':
        continue
    catalog_temp = descriptions_catalog[x]
    if len(x.split(str(catalog_temp), 1)) < 2:
        # print 'error line'
        continue
    catalog_descriptions_fixed.update({catalog_temp: x.split(str(catalog_temp), 1)[1]})

additional_descriptions = list(out.additional_description)
main_images = list(out.main_image)

catalog_ids = dict(zip(catalog, ids))
catalog_descriptions = dict(zip(catalog, descriptions))
catalog_additional_descriptions = dict(zip(catalog, additional_descriptions))
catalog_main_images = dict(zip(catalog, main_images))


class CarlislebeltsCrawl(CrawlSpider):
    name = "carlislebelts"

    allowed_domains = ['carlislebelts.com']

    start_urls = [
        'http://www.carlislebelts.com/product/search_products?productSearch=Synchro-Cog+Belt+HT&productSubmit=GO'
    ]

    def start_requests(self):
        for cat in catalog_descriptions_fixed:
            url = 'http://www.carlislebelts.com/product/search_products?productSearch={}&productSubmit=GO'.format(
                catalog_descriptions_fixed[cat]
            )
            yield scrapy.Request(
                url=url,
                dont_filter=True,
                callback=self.parse_search,
                meta={'catalog_number': cat}
            )

    def parse_search(self, response):
        if not response.xpath('//ul[@class="product-items"]//a/@href'):
            return
        url = 'http://www.carlislebelts.com' + response.xpath('//ul[@class="product-items"]//a/@href').extract()[0]
        return scrapy.Request(
            url=url,
            dont_filter=True,
            callback=self.parse_item,
            meta=response.meta
        )

    def parse_item(self, response):
        catalog_number = response.meta['catalog_number']

        item = UniversalItem()

        item['ids'] = catalog_ids[catalog_number]
        item['catalog_number'] = catalog_number
        item['image'] = catalog_main_images[catalog_number]
        item['description'] = catalog_descriptions[catalog_number]

        if str(catalog_additional_descriptions[catalog_number]) != 'nan':
            item['additional_description'] = catalog_additional_descriptions[catalog_number]
        else:
            made_in = re.compile('<a.*?>|<p>Backed by our.*?\p>|<p><img.*?\p>|\\n')
            additional_description = response.xpath('//div[@class="cms-edit-size"]/cmsitemreset/div').extract()[0]
            item['additional_description'] = re.sub(made_in, '', additional_description)
        if 'default' in catalog_main_images[catalog_number]:
            if response.xpath('//span[@class="prod-thumb selected"]/img/@src'):
                item['image'] = 'http://www.carlislebelts.com' + response.xpath('//span[@class="prod-thumb selected"]/img/@src').extract()[0]

        item['brochure'] = ''
        item['product_specs'] = ''

        item['brochure'] = 'http://www.carlislebelts.com' + \
                                 response.xpath('//div[@class="product-download"]/p[contains(text(), "Brochure")]/../a/@href').extract()[0]
        item['product_specs'] = 'http://www.carlislebelts.com' + \
                                response.xpath('//div[@class="product-download"]/p[contains(text(), "Product Specs")]/../a/@href').extract()[0]

        return item
