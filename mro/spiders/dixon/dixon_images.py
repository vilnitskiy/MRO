# -*- coding: utf-8 -*-
import pandas
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector

from mro.items import UniversalItem

class DixonImagesSpider(CrawlSpider):
    name = "dixon_images"
    allowed_domains = ["dixonvalve.com"]
    data = pandas.read_csv("mro/spiders/csv_data/Dixon/dixon_images.csv", sep=',')
    catalog = list(data.catalog_number)
    items = []

    # create list of urls from file
    urls = []
    for sku in catalog:
        urls.append('https://www.dixonvalve.com/product/' + str(sku))
    start_urls = urls

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        data = pandas.read_csv("spiders/csv_data/Dixon/dixon_images.csv", sep=',')
        catalog = list(data.catalog_number)
        ids = list(data.id)
        description = list(data.description)

        catalog_ids = dict(zip(catalog, ids))
        catalog_description = dict(zip(catalog, description))

        for sku in catalog:
            if str(sku) in response.xpath('//div[@id="product-specs"]').extract_first():
                if sku not in self.items:
                    item = UniversalItem()
                    item['ids'] = catalog_ids[sku]
                    item['catalog_number'] = sku
                    item['description'] = catalog_description[sku]
                    item['main_image'] = response.xpath('//img[@class="product-image"]/@src').extract_first()
                    item['response_url'] = response.url
                    self.items.append(sku)
                    return item
