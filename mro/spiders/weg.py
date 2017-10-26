# -*- coding: utf-8 -*-
import re
import urllib

import pandas as pd
import scrapy

from mro.items import WegItem

out = pd.read_csv("spiders/csv_data/Weg/weg.csv", sep=',')
catalog = list(out.catalog_number)
ids = list(out.id)
catalog_ids = dict(zip(catalog, ids))


class Weg(scrapy.Spider):
    name = "weg"

    def start_requests(self):
        for row in out['catalog_number']:
            yield self.request(row)

    def request(self, meta_row):
        row = urllib.quote_plus(str(meta_row).strip())
        url = 'http://www.weg.net/catalog/weg/US/en/search?text=' + row
        callback = lambda response: self.parse_item1(response, meta_row)
        errback = lambda failure: self.repeat(failure, meta_row)
        return scrapy.Request(url=url, callback=callback, dont_filter=True)

    def repeat(self, failure, meta_row):
        return self.request(meta_row)

    def error(self, row):
        item = WegItem()
        item['ids'] = catalog_ids[row]
        item['catalog_number'] = str(row)
        item['descr'] = ''
        item['add_descr'] = ''
        item['img_url'] = ''
        return item

    def parse_item1(self, response, meta_row):
        if 'search?text=' not in str(response.url):
            return self.parse_item2(response, meta_row)
        try:
            search_catagol_number = response.xpath(
                '//*[@id="page"]/div/div/div[3]/div[5]/div/div[3]/div[2]/table/tbody/tr[1]/td[3]/p/text()').extract_first().encode(
                'ascii', 'ignore').split(':')[1]
        except Exception:
            try:
                search_catagol_number = response.xpath(
                    '//*[@id="page"]/div/div/div[3]/div[5]/div[2]/div[3]/div[2]/table/tbody/tr[1]/td[3]/a/text()').extract_first()
                search_catagol_number = search_catagol_number if search_catagol_number else ''
            except Exception:
                return self.error(meta_row)
            else:
                if str(meta_row).strip() in search_catagol_number:
                    callback = lambda response: self.parse_item2(response, meta_row)
                    errback = lambda failure: self.repeat(failure, meta_row)
                    url = 'http://www.weg.net' + response.xpath(
                        '//*[@id="page"]/div/div/div[3]/div[5]/div/div[3]/div[2]/table/tbody/tr[1]/td[3]/a/@href').extract_first()
                    return scrapy.Request(url=url, callback=callback, errback=errback)
                else:
                    return self.error(meta_row)
        else:
            if search_catagol_number == str(meta_row).strip():
                callback = lambda response: self.parse_item2(response, meta_row)
                errback = lambda failure: self.repeat(failure, meta_row)
                url = 'http://www.weg.net' + response.xpath(
                    '//*[@id="page"]/div/div/div[3]/div[5]/div[2]/div[3]/div[2]/table/tbody/tr[1]/td[3]/a/@href').extract_first()
                return scrapy.Request(url=url, callback=callback, errback=errback)
            else:
                return self.error(meta_row)

    def construct_table1(self, table):
        text = table.xpath('div[1]').extract_first()
        text = text if text else ''
        head = table.xpath('h5').extract_first()
        table = table.xpath('div[2]').extract_first()
        table = re.sub(
            r'</tbody>(\n|\s)+</table>(\n|\s)+</div>(\n|\s)+<div class="col-xs-12 col-sm-6">(\n|\s)+<table class="table">(\n|\s)+<tbody>',
            '', table)
        table = table.replace('<div class="row product-info-specs">', '').replace('<div class="col-xs-12 col-sm-6">',
                                                                                  '').replace('</div>', '').strip()
        table = text + head + table + "<hr>"
        return table

    def construct_table2(self, response):
        index = 1
        content = ''
        for tabl in response.xpath('//*[@id="datasheet"]/div[1]/div'):
            table = tabl.xpath('.').extract_first()
            expression = '//*[@id="datasheet"]/ul/li[%s]/a/text()' % index
            index += 1
            head = response.xpath(expression).extract_first()
            head = "<div>" + head + "</div>" if head else ''
            table = re.sub(
                r'</tbody>(\n|\s)+</table>(\n|\s)+</div>(\n|\s)+<div class="col-xs-12 col-sm-4">(\n|\s)+<table class="table table-striped table-hover xtt-table-50 ">(\n|\s)+<tbody>',
                '', table)
            tabe_head = response.xpath('//*[@id="datasheet"]/div[1]/h4').extract_first()
            tabe_head = tabe_head if tabe_head else ''
            table = head + tabe_head + table + '<hr>'
            content = content + table
        features_head = response.xpath('//*[@id="datasheet"]/h4').extract_first()
        features = response.xpath('//*[@id="datasheet"]/div[2]/div/div/table').extract_first()
        features_full = features_head + features if features_head and features else ''
        return content + features_full

    def parse_item2(self, response, meta_row):
        ids = catalog_ids[meta_row]
        descr = response.xpath('//*[@id="page"]/div/div/section[1]/div[1]/h1/text()').extract_first()
        add_descr1 = self.construct_table1(response.xpath('//*[@id="page"]/div/div/section[1]/div[2]/div[2]'))
        add_descr2 = self.construct_table2(response)
        img = response.xpath('//*[@id="xtt-product-gallery"]/div/div/img/@src').extract_first()
        item = WegItem()
        item['ids'] = catalog_ids[meta_row]
        item['catalog_number'] = str(meta_row).strip()
        item['descr'] = descr
        item['add_descr'] = add_descr1 + add_descr2
        item['img_url'] = img
        return item
