# -*- coding: utf-8 -*-
import pandas
import scrapy
from mro.items import UniversalItem

class Durhammfg(scrapy.Spider):
    name = "durhammfg"
    allowed_domains = ["durhammfg.com", ]
    data = pandas.read_csv("spiders/csv_data/mfg/mfg.csv", sep=';')
    catalog_number = list(data.catalog_number)
    image_urls = list(data.img_url)
    images = dict(zip(catalog_number, image_urls))
    ids = dict(zip(catalog_number, list(data.id)))

    def start_requests(self):
        for catalog_number in self.catalog_number:
            if 'default' in self.images[catalog_number]:
                yield scrapy.Request(
                                url='http://www.durhammfg.com/search.html?searchterm={0}'.format(catalog_number), 
                                callback=self.wrapper(catalog_number)
                            )

    def wrapper(self, catalog_number):
        def parse_item(response):
            item_image = response.xpath('//td[@class="item_img"]/img/@src').extract_first()
            if item_image:
                if self.images.get(catalog_number) and 'default' in self.images[catalog_number]:
                    item = UniversalItem()
                    item['ids'] = self.ids[catalog_number]
                    item['catalog_number'] = catalog_number
                    item['img_url'] = item_image
                    return item
        return parse_item