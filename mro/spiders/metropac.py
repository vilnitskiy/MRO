# -*- coding: utf-8 -*-
import re

import pandas
import scrapy
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector

from mro.items import MetropacItem


class MetropacSpider(CrawlSpider):
    name = "metropac"
    allowed_domains = ["metropac.com"]
    items = []

    data = pandas.read_csv("spiders/csv_data/Metropac/tempus_111.csv", sep=',')
    track = ''

    start_urls = ['https://www.metropac.com/']

    def parse(self, response):
        return scrapy.Request(
            url='https://www.metropac.com/eserv/eclipse.ecl?FORMNAME=FX',
            dont_filter=True,
            callback=self.parse1
        )

    def parse1(self, response):
        cookie = response.xpath('//script').re('var trkNo = "(.+)"')[0]
        # print cookie
        url = 'https://www.metropac.com/eserv/eclipse.ecl'
        formdata = {
            'PROCID': 'WEBPROC.WOE.AUTH',
            'TRACKNO': cookie,
            # 'TRACKNO': 'J6543819402',
            'SEARCHSTR': '',
            'FX': 'FX',
            'VER': 'B',
            'WEB.COMPANY': '',
            'SITE.AUTH': '1',
            'BROWSER': 'NS',
            'D1': '33887',
            'D2': 'Larco1898',
            'savelogpw': '',
            'bypass': ''
        }
        # print '------------login--------------' + cookie
        self.track = cookie
        return scrapy.FormRequest(
            url=url,
            # errback=lambda failure: self.request(meta_row),
            dont_filter=True,
            formdata=formdata,
            callback=self.continue1
        )

    def continue1(self, response):
        self.track = response.xpath('//input[@name="TRACKNO"]/@value').extract_first()
        formdata = {
            'PROCID': 'WEBPROC.WOE.SELECT.ST',
            'TRACKNO': self.track,
            'SORTORDER': 'NAME',
            'D1': '33887',
            'SEARCH': '',
            'STYPE': 'NAME',
            'SEL.ADDR:33887.x': '6',
            'SEL.ADDR:33887.y': '5'
        }

        request = scrapy.FormRequest(
            url='https://www.metropac.com/eserv/eclipse.ecl',
            callback=self.start_req,
            formdata=formdata,
            dont_filter=True
        )
        request.cookies['login'] = '33887'
        request.cookies['pword'] = 'Larco1898'
        request.cookies['bypass'] = 'true'
        request.cookies['trackno'] = self.track
        return request

    def start_req(self, response):
        for row in self.data['catalog_number']:
            # row = self.data['catalog_number'][i]
            # prev = self.data['catalog_number'][i-1]
            yield self.request1(row)
            # for row, prev in zip(self.data['catalog_number'], self.data['catalog_number'][1:]):
            #     yield self.request1(row, prev)

    def request1(self, meta_row):
        row = str(meta_row).strip()
        # prev = str(prev).strip()
        url = 'https://www.metropac.com/eserv/eclipse.ecl'
        formdata = {
            'PROCID': 'WEBPROC.WOEB.MAIN',
            'TRACKNO': self.track,
            'SEARCH': row,
            'x': '1',
            'y': '1'
        }

        return scrapy.FormRequest(
            url=url,
            callback=self.parse_item0,
            dont_filter=True,
            formdata=formdata,
            meta={'meta_row': meta_row},
        )

    def parse_item0(self, response):
        url = 'https://www.metropac.com' + response.xpath('//script').re("document.location = '(.+)';")[0]
        return scrapy.Request(url=url, dont_filter=True, meta=response.request.meta, callback=self.parse_item_final)

    def parse_item_final(self, response):
        hxs = HtmlXPathSelector(response)
        catalog = list(self.data.catalog_number)
        prev_num = str(response.meta['meta_row']).strip()
        price = re.findall('<b>Retail:</b> \$&nbsp;(.+)&nbsp;ea', response.body)
        desc = response.xpath('//b[contains(text(), "Product Description")]/..').extract_first()

        print prev_num
        if prev_num and desc:
            if prev_num not in desc:
                return
        else:
            return
        if not price:
            return

        item = MetropacItem()
        item['catalog_number'] = str(response.meta['meta_row']).strip()
        item['retail'] = re.findall('<b>Retail:</b> \$&nbsp;(.+)&nbsp;ea', response.body)[0]
        item['your_price'] = re.findall('<b>Your Price:</b> \$&nbsp;(.+)&nbsp;ea', response.body)[0]
        return item
