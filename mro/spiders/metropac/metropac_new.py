# -*- coding: utf-8 -*-
import re
import scrapy
from mro.BaseSpiders.base_spiders import BaseMroSpider
import time


class Martin(BaseMroSpider):
    name = "metropac_new"
    output_filename = 'metropac_result.csv'
    token = 'J1835425849'
    search_url = 'https://www.metropac.com/eserv/eclipse.ecl?PROCID=WEBDISP.WOEB.MAIN&TRACKNO={}&SEARCH={}&CLEV=4'
    path_to_data = 'mro/spiders/csv_data/Metropac/Product_2018-2-4 (1).csv'
    separator = ','
    output_fields = ('id', 'catalog_number', 'your price')
    base_cookies = {
        'trackno': token,
        'login': '33887',
        'pword': 'Larco1898',
        'bypass': False
    }
    index = 0

    def start_requests(self):
        for row in self.catalog:
            yield self.request(row)

    def request(self, row):
        time.sleep(3)
        url = 'https://www.metropac.com/eserv/eclipse.ecl'
        formdata = {
            'PROCID': 'WEBPROC.WOEB.MAIN',
            'TRACKNO': self.token,
            'SEARCH': row,
            'x': '9',
            'y': '12'
        }
        return scrapy.FormRequest(
            url=url,
            callback=self.next_request,
            dont_filter=True,
            formdata=formdata,
            meta={'row': row},
            cookies=self.base_cookies,
        )

    def next_request(self, response):
        row = response.meta['row']
        #time.sleep(0.4)
        return scrapy.Request(url=self.search_url.format(self.token, row),
                                 callback=self.parse_item,
                                 cookies=self.base_cookies,
                                 meta=response.meta,
                                 dont_filter=True
                                 )

    def parse_item(self, response):
        catalog = response.meta['row']
        descr = response.xpath('//b[text()="Product Description"]/..').extract_first()
        price = response.xpath('//b[text()="Your Price:"]/../text()').extract()[-1]
        if price and descr:   
            if catalog in descr:
                self.index = 0
                return self.create_item(self.catalog_id[str(catalog)], catalog, price.strip())
            else:
                self.index += 1
                if self.index >=5:
                    self.index = 0
                    return self.create_item(self.catalog_id[str(catalog)], catalog, price.strip())
                return self.request(catalog)




