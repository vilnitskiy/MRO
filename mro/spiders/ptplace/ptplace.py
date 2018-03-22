# -*- coding: utf-8 -*-
import json
import re
import pandas as pd
import scrapy
from mro.BaseSpiders.base_spiders import BaseMroSpider
from scrapy.exceptions import CloseSpider



class Ptplace(BaseMroSpider):
    name = "ptplace"
    search_url = 'https://www.ptplace.com/ptp/do/productDetail?partNum={}&srcCode=0230&doNewSearch=true&referencePage=productSearch&navbartype=Store&selectedcountry=USA&viewstore=false&selectedstore=SchaefflerGroup&bflag=false&selectedlanguage=English'
    path_to_data = 'mro/spiders/csv_data/ptplace/Product_2018-3-1 (FAG) (1).csv'
    separator = ','
    output_fields = ('id', 'catalog_number', 'attributes')
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
    }

    def start_requests(self):
        for row in self.catalog:
            yield scrapy.Request(url=self.search_url.format(row.replace('.', '-')),
                                 callback=self.parse_item,
                                 cookies=self.base_cookies,
                                 meta={'row': row}
                                 )

    def parse_item(self, response):
        catalog = response.meta['row']
        if catalog.replace('.', '-') in (response.xpath('//*[@id="contentForm"]/h2/text()').extract_first() or ''):
            catalog = response.meta['row']
            token = response.xpath('//input[@name="org.apache.struts.taglib.html.TOKEN"]/@value').extract_first()
            if not token:
                raise CloseSpider('No token!')
            url = 'https://www.ptplace.com/ptp/do/productDetail'
            formdata = {
                'org.apache.struts.taglib.html.TOKEN': token,
                'selectedcountry':'USA',
                'selectedlanguage':'English',
                'viewstore':'false',
                'selectedstore':'SchaefflerGroup',
                'navbartype':'Store',
                'bflag':'false',
                'partNum': catalog.replace('.', '-'),
                'srcCode':'0230',
                'quantityChanged': '',
                'icon.visibleToVisitors':'true',
                'productULF.lastOrderEntryPage':'productDetail',
                'productULF.UL(1).quantity': '',
                'productULF.UL(1).selWPC':'7001;02',
                'jsDefaultWarehouse':'7001;02',
                'jsUserChosenWarehouse':'7001',
                'productAttributesButton':'Product Attributes',
                'ARCANOL-MULTI3-400G|||0230':'on',
                'PULLER-2ARM200|||0230':'on',
                'PULLER-3ARM160|||0230':'on',
                'TEMP-CHECK-PRO|||0230':'on'
            }
            return scrapy.FormRequest(
                url=url,
                callback=self.next_request,
                dont_filter=True,
                formdata=formdata,
                meta=response.meta,
                cookies=self.base_cookies,
            )

    def next_request(self, response):
        catalog = response.meta['row']
        attr = ''
        for tr in response.xpath('//table[@id="prodDetailTable" and @class="lineitems"]/tbody/tr'):
            name = (tr.xpath('./td[1]/text()').extract_first() or tr.xpath('./th[1]/text()').extract_first()).strip()
            value = (tr.xpath('./td[2]/text()').extract_first() or tr.xpath('./th[2]/text()').extract_first()).strip()
            attr += name + ':' + value + '|'
        return self.create_item(self.catalog_id[catalog], catalog, attr)





