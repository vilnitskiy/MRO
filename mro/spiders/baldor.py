# -*- coding: utf-8 -*-
import pandas
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector

from mro.items import BaldorImgItem


class BaldorSpider(CrawlSpider):
    name = "baldor"
    allowed_domains = ["baldor.com"]
    data = pandas.read_csv("spiders/csv_data/Baldor/Product.csv", sep=',')
    catalog = list(data.catalog_number)
    items = []

    # create list of urls from file
    urls = []
    for sku in catalog:
        urls.append('http://www.baldor.com/catalog/' + str(sku))

    start_urls = urls

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        data = pandas.read_csv("csv_data/Baldor/Product.csv", sep=',')
        catalog = list(data.catalog_number)
        ids = list(data.id)
        descr = list(data.description)

        catalog_ids = dict(zip(catalog, ids))
        catalog_descr = dict(zip(catalog, descr))

        sku = response.url.rsplit('/', 1)[-1]

        if str(sku) in response.xpath('//div[@class="page-title"]').extract_first():
            img = response.xpath('//img[@class="product-image"]/@data-src').extract_first()
            if sku not in self.items:
                if img != '/api/images/451' or response.xpath(
                        '//table[@class="detail-table"]//tr[3]/td/text()').extract_first() != None or response.xpath(
                        '//table[@class="detail-table"]').re('(\d+.\d+ LB)'):
                    item = BaldorImgItem()
                    item['ids'] = catalog_ids[sku]
                    item['description'] = catalog_descr[sku]
                    item['catalog_number'] = sku
                    if img != '/api/images/451':
                        item['main_image'] = 'http://www.baldor.com' + img
                    else:
                        item['main_image'] = None
                    if response.xpath('//table[@class="detail-table"]//tr[3]/td/text()').extract_first():
                        item['ship_weight'] = response.xpath(
                            '//table[@class="detail-table"]//tr[3]/td/text()').extract_first()
                    else:
                        item['ship_weight'] = response.xpath('//table[@class="detail-table"]').re('(\d+.\d+ LB)')[0]
                    self.items.append(sku)
                    return item
