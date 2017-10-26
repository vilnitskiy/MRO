# -*- coding: utf-8 -*-
import pandas as pd
import scrapy
from mro.items import BaldorvipItem
from scrapy.http import FormRequest
import yaml
import re

out = pd.read_csv("spiders/csv_data/Baldor/baldor.csv", sep=',')
catalog = list(out.catalog_number)
ids = list(out.id)
catalog_ids = dict(zip(catalog, ids))


class Baldor(scrapy.Spider):
    name = "baldorvip"

    def start_requests(self):
        for row in out['catalog_number']:
            url = 'https://www.baldorvip.com/Product/Detail/' + row
            yield scrapy.Request(url=url,callback=self.parse_item, meta={'row': row})

    def parse_item(self, response):
        data1 = response.xpath('//*').re(r'\)\.load\("/Product/LoadPartsListTab", {(.+)}')[0]
        data1 = yaml.load("{"+str(data1)+"}")
        data2 = response.xpath('//*').re(r'\)\.load\("/Product/LoadPerformanceTab", {(.+)}')[0]
        data2 = yaml.load("{"+str(data2)+"}")        
        result = str(response.xpath('//*[@class="verticalTable"]/tbody').extract_first())
        return FormRequest(url="https://www.baldorvip.com/Product/LoadSpecsTab",
                    formdata={'MaterialNumber': response.meta['row']},
                    callback=self.parse_item1, meta={'row': response.meta['row'], 'res': result, 'data2': data2, 'data1':data1})


    def parse_item1(self, response):
        result = str(response.meta['res']) + str(response.xpath('//*').extract_first().encode('ascii', 'ignore'))
        return FormRequest(url="https://www.baldorvip.com/Product/LoadPerformanceTab",
                    formdata=response.meta['data2'],
                    callback=self.parse_item2, meta={'row': response.meta['row'], 'res': result, 'data2': response.meta['data2'], 'data1':response.meta['data1']})

    def parse_item2(self, response):
        result = str(response.meta['res']) + str(response.xpath('//*[@id="PerfDataList"]/option/text()').extract_first())
        return FormRequest(url="https://www.baldorvip.com/Product/LoadPartsListTab",
                    formdata=response.meta['data1'],
                    callback=self.parse_item3, meta={'row': response.meta['row'], 'res': result})


    def parse_item3(self, response):
        item = BaldorItem()
        item['ids'] = catalog_ids[response.meta['row']]
        item['catalog_number'] = response.meta['row']
        result = str(response.meta['res']) + str(response.xpath('//*/form').extract_first())
        item['additional_descr'] = result
        return item



