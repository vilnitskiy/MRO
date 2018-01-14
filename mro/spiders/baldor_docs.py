# -*- coding: utf-8 -*-
import re

import pandas as pd
import scrapy

from mro.items import UniversalItem

out = pd.read_csv("spiders/csv_data/Baldor/diff_baldor.csv", sep=',')
catalog = [str(item).strip() for item in list(out.catalog_number)]
description = list(out.description)
ids = list(out.id)
catalog_descr = dict(zip(catalog, description))
catalog_ids = dict(zip(catalog, ids))


class Mcr(scrapy.Spider):
    name = "baldor_docs"

    def start_requests(self):
        for row in catalog:
            yield self.request(row)

    def request(self, row):
        url = 'http://www.baldor.com/catalog/' + row
        return scrapy.Request(url=url,
                              callback=self.parse_item,
                              dont_filter=True,
                              meta={'row': row}
                              )

    def create_item(self, row, img, doc_name, doc_url, specs):
        item = UniversalItem()
        item['ids'] = catalog_ids[row]
        item['catalog_number'] = row
        item['description'] = catalog_descr[row]
        item['img'] = img
        item['doc_name'] = doc_name
        item['doc_url'] = doc_url
        item['specs'] = specs
        return item

    def construct_table(self, table):
        table = table.replace('<div class="section detail-table product-overview">', '<table>')
        table = re.sub(r'</div>(\n|\s)+<div class="col span_1_of_2">', '', table)
        table = table.replace('<div class="col span_1_of_2">', '')
        table = re.sub(r'</div>(\n|\s)+</div>(\n|\s)+</div>(\n|\s)+</div>', '</div></table></div>', table)
        table = re.sub(r'</div>(\n|\s)+<div>', '</tr><tr>', table)
        table = table.replace('</div></table>', '</tr></table>')
        table = table.replace('<div>', '<tr>')
        table = table.replace('<span class="label">', '<td>').replace('<span class="value">', '<td>')
        table = table.replace('</span>', '</td>')
        return table

    def custom_extractor(self, response, expression):
        data = response.xpath(expression).extract_first()
        return data if data else ''

    def parse_item(self, response):
        row = response.meta['row']
        img = self.custom_extractor(response, '//*[@id="catalog-detail"]/img/@data-src')
        img = 'http://www.baldor.com' + img + '?bc=white&as=1&h=256&w=256' if img != '/api/images/451' else ''
        specs = self.custom_extractor(response, '//div[@data-tab="specs"]')
        specs = self.construct_table(specs) if specs != '' else ''
        key = response.xpath('//*[@id="nav-desktop-breadcrumb"]/ul/li/a/text()').extract()[-1]
        key_tire = 0
        try:
            int(key.split()[-1])
        except Exception:
            pass
        else:
            key_tire = key.replace(' ', '-')
        key_upper = key.upper()

        doc_name, doc_url = '', ''

        expression = '//a[@class="recordClick" and text()="%s"]' % key
        item = response.xpath(expression)
        if not item:
            expression = '//a[@class="recordClick" and text()="%s"]' % key_upper
            item = response.xpath(expression)
        if not item and key_tire:
            expression = '//a[@class="recordClick" and text()="%s"]' % key_tire
            item = response.xpath(expression)

        if not item:
            expression = '//a[@class="recordClick" and  starts-with(text(), "%s")]' % key
            item = response.xpath(expression)
        if not item:
            expression = '//a[@class="recordClick" and  starts-with(text(), "%s")]' % key_upper
            item = response.xpath(expression)
        if not item and key_tire:
            expression = '//a[@class="recordClick" and  starts-with(text(), "%s")]' % key_tire
            item = response.xpath(expression)

        if not item:
            expression = '//a[@class="recordClick" and text()="Dodge %s"]' % key
            item = response.xpath(expression)
        if not item and key_tire:
            expression = '//a[@class="recordClick" and text()="Dodge %s"]' % key_tire
            item = response.xpath(expression)

        if not item:
            expression = '//a[@class="recordClick" and contains(text(), "Dodge") and contains(text(), "%s")]' % key
            item = response.xpath(expression)
        if not item:
            expression = '//a[@class="recordClick" and contains(text(), "Dodge") and contains(text(), "%s")]' % key_upper
            item = response.xpath(expression)
        if not item and key_tire:
            expression = '//a[@class="recordClick" and contains(text(), "Dodge") and contains(text(), "%s")]' % key_tire
            item = response.xpath(expression)

        if not item:
            expression = '//a[@class="recordClick" and contains(text(), "%s")]' % key
            item = response.xpath(expression)
        if not item:
            expression = '//a[@class="recordClick" and contains(text(), "%s")]' % key_upper
            item = response.xpath(expression)
        if not item and key_tire:
            expression = '//a[@class="recordClick" and contains(text(), "%s")]' % key_tire
            item = response.xpath(expression)

        if not item:
            key_split = key.split()
            for part in key_split:
                expression = '//a[@class="recordClick" and contains(text(), "%s")]' % part
                item = response.xpath(expression)
                if item:
                    break

        if not item:
            item = response.xpath('//ul[@class="list-icon-document"]/li[1]/a')

        doc_name = self.custom_extractor(item, './text()')
        doc_url = item.xpath('./@href').extract_first()
        doc_url = response.urljoin(doc_url) if doc_url else ''

        return self.create_item(row, img, doc_name, doc_url, specs)
