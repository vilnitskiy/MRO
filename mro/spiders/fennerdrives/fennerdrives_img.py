# -*- coding: utf-8 -*-
import pandas
from scrapy.spiders import CrawlSpider
from scrapy import Request
from mro.items import UniversalItem


class Fennerdrives(CrawlSpider):
    name = "fennerdrives_img"
    allowed_domains = ["fennerdrives.com", ]
    data = pandas.read_csv("mro/spiders/csv_data/Fennerdrives/Fenner_Drives_images.csv", sep=';')
    catalog_number = list(data.catalog_number)
    main_image = list(data.main_image)
    images = dict(zip(catalog_number, main_image))
    ids = dict(zip(catalog_number, list(data.id)))

    def start_requests(self):
        for catalog_number in self.catalog_number:
            if 'default' in self.images[catalog_number]:
                yield Request(
                                url='http://www.fennerdrives.com/search/?q={0}'.format(catalog_number), 
                                callback=self.wrapper(catalog_number)
                            )

    def wrapper(self, catalog_number):
        def parse_item(response):
            # description = response.xpath('//div[@class="description"]/text()').extract_first()
            # description = description.replace('\r\n\t\r\n        ', '').replace('\r\n    \r\n', '')
            main_image = response.xpath('//div[@class="media wl-cf"]/div[@class="primary wl-cf"]/a/@href').extract_first()
            if main_image:
                if self.images.get(catalog_number) and 'default' in self.images[catalog_number]:
                    item = UniversalItem()
                    item['images'] = main_image
                    item['catalog_number'] = catalog_number
                    item['ids'] = self.ids[catalog_number]
                    return item
        return parse_item
