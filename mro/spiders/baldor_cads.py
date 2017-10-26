# -*- coding: utf-8 -*-
import shutil
import urllib2

import pandas
from scrapy.contrib.spiders import CrawlSpider

from mro.items import BaldorCadItem


class BaldorSpider(CrawlSpider):
    name = "baldor_cads"
    allowed_domains = ["baldor.com"]

    data = pandas.read_csv("spiders/csv_data/Baldor/Product.csv", sep=',')
    catalog = list(data.catalog_number)
    ids = list(data.id)
    descr = list(data.description)

    catalog_ids = dict(zip(catalog, ids))
    catalog_descr = dict(zip(catalog, descr))

    items = []

    # create list of urls from file
    urls = []
    for sku in catalog:
        urls.append('http://www.baldor.com/catalog/' + str(sku))

    start_urls = urls

    # start_urls = ['http://www.baldor.com/catalog/136988']

    def parse(self, response):
        if response.xpath('//input[@name="drwType"]') and response.xpath('//div[@class="section cadfiles"]/@ng-init'):
            if '2D' in response.xpath('//div[@class="section cadfiles"]/@ng-init').extract()[0]:
                return self.parse_item(response)

    def parse_item(self, response):
        sku = response.url.rsplit('/', 1)[-1]

        item = BaldorCadItem()

        item['description'] = self.catalog_descr[int(sku)]
        item['ids'] = self.catalog_ids[int(sku)]
        item['catalog_number'] = sku

        pdf_2d_url = 'http://www.baldor.com/api/products/cadfile/PDFDATASHEET/{}/{}'.format(sku, sku)
        dxf_2d_url = 'http://www.baldor.com/api/products/cadfile/DXF2D-AUTOCAD%20VERSION%202013/{}/{}'.format(sku, sku)
        dxf_3d_url = 'http://www.baldor.com/api/products/cadfile/DXF3D-AUTOCAD%20VERSION%202013/{}/{}'.format(sku, sku)

        # 2D PDF
        try:
            request = urllib2.Request(pdf_2d_url)
            link = urllib2.urlopen(request)
            url = link.read().replace('"', '')

            request = urllib2.Request(url)
            resp = urllib2.urlopen(request)

            file_name = '%s_pdf2d.zip' % sku
            with open('baldor_download/' + file_name, 'wb') as file:
                shutil.copyfileobj(resp.fp, file)
        except Exception:
            item['pdf_2d'] = ''
        else:
            item['pdf_2d'] = file_name

        # 2D DXF
        try:
            request = urllib2.Request(dxf_2d_url)
            link = urllib2.urlopen(request)
            url = link.read().replace('"', '')

            request = urllib2.Request(url)
            resp = urllib2.urlopen(request)
            file_name = '%s_dxf2d.zip' % sku
            with open('baldor_download/' + file_name, 'wb') as file:
                shutil.copyfileobj(resp.fp, file)
        except Exception:
            item['dxf_2d'] = ''
        else:
            item['dxf_2d'] = file_name

        # 3D DXF
        try:
            request = urllib2.Request(dxf_3d_url)
            link = urllib2.urlopen(request)
            url = link.read().replace('"', '')

            request = urllib2.Request(url)
            resp = urllib2.urlopen(request)
            file_name = '%s_dxf3d.zip' % sku
            with open('baldor_download/' + file_name, 'wb') as file:
                shutil.copyfileobj(resp.fp, file)
        except Exception:
            item['dxf_3d'] = ''
        else:
            item['dxf_3d'] = file_name

        return item
