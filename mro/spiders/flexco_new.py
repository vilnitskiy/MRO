# -*- coding: utf-8 -*-
import pandas as pd
import scrapy
import urllib
import urllib2
from mro.items import EItem
from scrapy.http import FormRequest
import re

out = pd.read_csv("spiders/csv_data/flexco/0695487001508855201_0.csv", sep=',')
catalog_item_codes = [str(item).strip() for item in out.item_code]
ids = list(out.id)
description = list(out.description)
ordering_number = list(out.ordering_number)
item_codes_ids = dict(zip(catalog_item_codes, ids))
item_codes_description = dict(zip(catalog_item_codes, description))
item_code_ordering_number = dict(zip(catalog_item_codes, ordering_number))
'''
control = pd.read_csv("result_flexco.csv", sep=',')
control_item_codes = [str(item).strip() for item in out.item_code]
'''
f = open('spiders/csv_data/flexco/viewstage.txt', 'r')
viewstage = f.read()
f.close()

formdata = {
        'ctl00_TreeView1_ExpandState':"",
        'ctl00_TreeView1_SelectedNode':"",
        '__EVENTTARGET':"ctl00$ContentPlaceHolder1$dgItemSelection",
        '__EVENTARGUMENT':"Page$Next",
        'ctl00_TreeView1_PopulateLog':"",
        '__LASTFOCUS':"",
        '__VIEWSTATE': viewstage,
        '__VIEWSTATEGENERATOR':"9414B4BC",
        'ctl00$ContentPlaceHolder1$hidBeltThickness':"",
        'ctl00$ContentPlaceHolder1$txtBeltThicknessInput':"",
        'ctl00$ContentPlaceHolder1$dgItemSelection$ctl02$txtQuantity':"",
        'ctl00$ContentPlaceHolder1$dgItemSelection$ctl03$txtQuantity':"",
        'ctl00$ContentPlaceHolder1$dgItemSelection$ctl04$txtQuantity':"",
        'ctl00$ContentPlaceHolder1$dgItemSelection$ctl05$txtQuantity':"",
        'ctl00$ContentPlaceHolder1$dgItemSelection$ctl06$txtQuantity':"",
        'ctl00$ContentPlaceHolder1$ddlPageSize':"5",
        'ctl00$hdSessionTimeOut':""
        }


class Weg(scrapy.Spider):
    name = "e-services"

    start_urls = ['https://www.e-services.flexco.com/eCollaboration/ecatalog/aspx/ParameterListing.aspx?Source=&IndustryID=0&ProductID=2762']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_item, meta={'proxy': '108.59.14.208:13041'})

    def parse_item(self, response):
        item_codes = response.xpath('//tr[@class="paramvalues"]/td[3]/text()').extract()
        print item_codes
        for code in item_codes:
            if code in catalog_item_codes:
                url = response.xpath('//td[@class="formnames" and text()="%s"]/../td[6]/a/@href' % code).extract_first()
                yield scrapy.Request(url=response.urljoin(url), callback=self.parse_item2, meta={'code': code})

        if response.xpath('//a[text()="Next"]'):
            yield FormRequest(url=response.url, 
                            callback=self.parse,
                            #errback=lambda failure: self.request(row),
                            dont_filter=True,
                            formdata=formdata
                            )



    def parse_item2(self, response):
        code = response.meta['code']
        descr = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_dlSpecs"]').extract_first()
        E = EItem()
        E['ids'] = item_codes_ids[code]
        E['description'] = item_codes_description[code]
        E['item_code'] = code
        E['add_descr'] = descr
        E['ordering_number'] = item_code_ordering_number[code]
        return E