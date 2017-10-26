# -*- coding: utf-8 -*-
import re

import pandas
import scrapy
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector

from mro.items import GrundfosItem


class GrundfosSpider(CrawlSpider):
    name = "grundfos"
    allowed_domains = ["grundfos.com"]
    items = []
    pr = True
    cookies = {
        'AMCVS_BA23678254F61E630A4C98A5@AdobeOrg': "1",
        'AMCV_BA23678254F61E630A4C98A5@AdobeOrg': "1099438348|MCIDTS|17395|MCMID|12550951087790814574253316757767919054|MCAAMLH-1503513925|6|MCAAMB-1503519939|NRX38WO0n5BH8Th-nqAG_A|MCOPTOUT-1502922339s|NONE|MCAID|NONE|MCSYNCSOP|411-17402|vVersion|2.1.0",
        'Grundfos_cookies_allowed': "true",
        'Grundfos_cookies_allowed': "true",
        'JSESSIONID': "891d0322-71bd-428d-819a-8813f09dfec1",
        'PD_STATEFUL_cc2f5a84-c098-11e3-9e79-e41f13722840': "product-selection.grundfos.com",
        'QSI_HistorySession': "http://product-selection.grundfos.com/product-detail.product-detail.html?from_suid=1502489555170014795914021288548&hits=1&productnumber=91122125&qcid=260408212&searchstring=91122125~1502915142120|http://product-selection.grundfos.com/product-detail.product-detail.html?from_suid=1502489555170014795914021288548&hits=1&productnumber=91122125&qcid=238934806&searchstring=91122125~1502915158815",
        'QSI_SI_0U87T6pBKe14FUx_intercept': "true",
        '_sdsat_Report Suite': "gfglobalprod,gfnewgpuprod",
        'addTo': "{}",
        'gpv_pn': "GPU:product-selection:detail",
        'mbox': "PC#cf4e34a05739458cbb09fb7e4f3d4707.26_18#1504124750|check#true#1502915210|session#207c07fde35e48849d94651c4c30d7ee#1502917010",
        'projectsSession': "{}",
        'recent': "{}",
        's_cc': "true",
        's_ppv': "GPU%3Aproduct-selection%3Adetail,61,61,1153,1301,372,1366,768,1,P",
        's_ppvl': "GPU%3Aproduct-selection%3Adetail,61,61,1153,1301,372,1366,768,1,P",
    }

    data = pandas.read_csv("spiders/csv_data/Grundfos/grundfox_additional_descriptions_work.csv", sep=',')
    catalog = [str(item).strip() for item in list(data.catalog_number)]
    ids = list(data.id)
    catalog_ids = dict(zip(catalog, ids))
    start_urls = []

    for number in list(data.catalog_number):
        start_urls.append(
            'http://product-selection.grundfos.com/product-detail.product-detail.html?hits=1&productnumber=' + str(
                number))

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, cookies=self.cookies, callback=self.parse)

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        data = pandas.read_csv("spiders/csv_data/Grundfos/grundfox_additional_descriptions_work.csv", sep=',')
        catalog = list(data.catalog_number)

        number = re.search('productnumber=(.+)', response.url).group(1)

        if not response.xpath('//h1[@id="product-details-title"]/text()').extract():
            return

        item = GrundfosItem()

        item['catalog_number'] = number
        print response.xpath('//div[@id="imageContainer"]/img/@src').extract()
        if response.xpath('//div[@id="imageContainer"]/img/@src').extract()[0] != '':
            item[
                'image'] = 'http://net.grundfos.com/RestServer/imaging/product?productnumber={}&frequency=60&languagecode=RUS&productrange=gmo&searchdomain=SALEABLE&unitsystem=4'.format(
                number)
        else:
            return
        item['description'] = response.xpath('//h1[@id="product-details-title"]/text()').extract()[0]
        specs = response.xpath('//div[@id="specifications"]').extract()[0]
        cleanr = re.compile('<a.*?>')
        cleanr1 = re.compile('</a>')
        without_links = re.sub(cleanr, '', specs)
        without_links = re.sub(cleanr1, '', without_links)
        item['specifications'] = without_links
        item['ids'] = self.catalog_ids[number]

        return item
