# -*- coding: utf-8 -*-
import HTMLParser
import re
import urllib

import pandas as pd
import scrapy

from mro.items import CrownItem

out = pd.read_csv("spiders/csv_data/Crown/Crown_images_&_descr.csv", sep=',')
catalog = [str(item).strip() for item in list(out.catalog_number)]
sku = [str(item).strip() for item in list(out.sku)]
descr = [str(item).strip() for item in list(out.description)]
ids = list(out.id)
catalog_ids = dict(zip(catalog, ids))
catalog_descr = dict(zip(catalog, descr))
catalog_sku = dict(zip(catalog, sku))


class Mcr(scrapy.Spider):
    name = "crown"

    def start_requests(self):
        for row in catalog:
            yield self.request(row)

    def request(self, row):
        product_descr = catalog_descr[row]
        sku = catalog_sku[row]
        key = re.findall(r'%s - (\S+) ' % sku, product_descr)[0]

        url = 'http://crown-mats.com/?s=' + urllib.quote_plus(key) + '&lang=en'
        return scrapy.Request(url=url,
                              callback=self.parse_item,
                              errback=lambda failure: self.request(row),
                              dont_filter=True,
                              meta={'row': row}
                              )

    def create_item(self, row, img_url, doc_url, add_descr):
        item = CrownItem()
        item['ids'] = catalog_ids[row]
        item['catalog_number'] = row
        item['img'] = img_url
        item['name'] = 'Spec Sheet'
        item['sku'] = catalog_sku[row]
        item['url'] = doc_url
        item['description'] = catalog_descr[row]
        item['additional_description'] = add_descr
        return item

    def custom_extractor(self, response, expression):
        data = response.xpath(expression).extract_first()
        return data if data else ''

    def parse_item(self, response):
        row = response.meta['row']
        product_descr = catalog_descr[row]
        if not response.xpath('//div[@class="error-page"]').extract_first():
            for item in response.xpath('//*[@id="posts-container"]/div'):
                key = item.xpath('./div[3]/h2/a/text()').extract_first()
                if key and (key.lower() in product_descr.lower()):
                    url = item.xpath('./div[3]/h2/a/@href').extract_first()
                    return scrapy.Request(url=url,
                                          callback=self.parse_item2,
                                          errback=lambda failure: self.request(row),
                                          dont_filter=True,
                                          meta={'row': row}
                                          )
        '''
        else:
            return self.create_item(row, '', '', '')
        '''

    def extract_data(self, response, color):
        if color != 1:
            expression = '//option[text()="%s"]/@value' % color
            color_key = response.xpath(expression).extract_first()
            data = response.xpath('//form[@class="variations_form cart"]/@data-product_variations').extract_first()
            html_parser = HTMLParser.HTMLParser()
            data = html_parser.unescape(data)
            data = re.findall(r'"%s"},"image_src":"(\S+)","image_link":' % color_key, data)[0]
            img = data.replace('/', '')
        else:
            img = response.xpath('//*[@id="slider"]/ul/li/a/img/@src').extract()[0]
        descr = self.custom_extractor(response, '//div[@itemprop="description"]')
        descr = descr.split('<p></p>')[0]
        add_info = self.custom_extractor(response, '//*[@id="tab-additional_information"]')
        tech_data = self.custom_extractor(response, '//*[@id="tab-product_editor_996_tab"]')
        pdf = self.custom_extractor(response, '//*[@id="tab-product_editor_3173_tab"]/p/a/@href')
        add_descr = descr + add_info + tech_data
        return img, add_descr, pdf

    def custom_split(self, item, expression):
        item = item.split(expression)
        return item[0] if len(item) == 1 else item[1]

    def parse_item2(self, response):
        row = response.meta['row']
        product_descr = catalog_descr[row]
        pages_sku = response.xpath('//span[@class="sku"]/text()').extract_first()

        # pattern row in next spider
        pattern_row = response.xpath('//th[text()="Pattern"]/../td/p/text()').extract_first()
        if pattern_row:
            return

        sku_in_description = self.custom_extractor(response, '//div[@itemprop="description"]/p[4]')

        if (catalog_sku[row] in pages_sku) or (catalog_sku[row] in sku_in_description):
            colors_row = response.xpath('//th[text()="Colors"]/../td/p/text()').extract_first()
            color_list = colors_row.split(', ')
            one_color = False
            if len(color_list) < 2:
                one_color = True
            color_list_with_slash = []
            for color in color_list:
                if ("/" in color) or ('&' in color):
                    color_list_with_slash.append(color)
            color_list_with_slash = set(color_list_with_slash)
            color_list_without_slash = set(color_list) - color_list_with_slash
            for color in color_list_with_slash:
                if (color in product_descr) or (color.replace(' & ', '/') in product_descr):
                    color = 1 if one_color else color
                    img, add_descr, pdf = self.extract_data(response, color)
                    return self.create_item(row, img, pdf, add_descr)
            for color in color_list_without_slash:
                if color in product_descr:
                    color = 1 if one_color else color
                    img, add_descr, pdf = self.extract_data(response, color)
                    return self.create_item(row, img, pdf, add_descr)
