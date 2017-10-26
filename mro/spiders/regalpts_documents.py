# -*- coding: utf-8 -*-
import pandas as pd
import scrapy
from scrapy.http import FormRequest

from mro.items import RegalptsDocumentsItem

out = pd.read_csv("spiders/csv_data/Regal/Regal_Beloit_Documents.csv", sep=',')
catalog = [str(item).strip() for item in list(out.catalog_number)]
brand = [item.strip() for item in list(out.Brand)]
ids = list(out.id)
catalog_ids = dict(zip(catalog, ids))
catalog_brand = dict(zip(catalog, brand))
f = open('spiders/csv_data/additions/viewstage.txt', 'r')
viewstage = f.read()
f.close()


class RegalptsDocsCrawl(scrapy.Spider):
    name = "regalpts_docs"

    def start_requests(self):
        for row in catalog:
            yield self.request(row)

    def request(self, row):
        url = 'http://edge.regalpts.com/EDGE/CAD/Default.aspx?SS=yes'
        formdata = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': viewstage,
            '__VIEWSTATEGENERATOR': 'CC83E274',
            '__EVENTVALIDATION': '/wEWBgL4+JvjBALjqMbGAQKW/Y24DgLJ/9mgDgKnipiBAQLyy5/lAuF2uu8b/BgziUqSvX9FGHOhGpdW',
            'ctl00_Master_ContentPlaceHolder1_MenuPanel_ClientState': '{"expandedItems":["0"],"logEntries":[],"selectedItems":[]}',
            'ctl00$Master$ContentPlaceHolder1$ContentPlaceHolderMain$TextBoxPartNumber': row,
            'ctl00$Master$ContentPlaceHolder1$ContentPlaceHolderMain$ButtonPartSearch': 'SEARCH >',
            'ctl00_Master_ContentPlaceHolder1_ContentPlaceHolderMain_RadTreeViewProductLine_ClientState': '{"expandedNodes":[],"collapsedNodes":[],"logEntries":[],"selectedNodes":[],"checkedNodes":[],"scrollPosition":0}',
            'ctl00_Master_ContentPlaceHolder1_ContentPlaceHolderMain_RadWindowOpenPDF_ClientState': '',
            'ctl00_Master_ContentPlaceHolder1_ContentPlaceHolderMain_RadWindowManagerOpenPDF_ClientState': '',
            'ctl00_Master_ContentPlaceHolder1_RadWindowNemaStandards_ClientState': '',
            'ctl00_Master_ContentPlaceHolder1_RadWindowIECStandards_ClientState': '',
            'ctl00_Master_ContentPlaceHolder1_RadWindowManagerPopups_ClientState': ''
        }
        return FormRequest(url=url,
                           callback=self.parse_item,
                           errback=lambda failure: self.request(row),
                           dont_filter=True,
                           formdata=formdata,
                           meta={'row': row}
                           )

    def create_item(self, row, url, name):
        item = RegalptsDocumentsItem()
        item['ids'] = catalog_ids[row]
        item['brand'] = catalog_brand[row]
        item['catalog_number'] = row
        item['name'] = name
        item['url'] = url
        return item

    def parse_item(self, response):
        row = response.meta['row']
        if 'Group' in response.url:
            expression = '//a[text()="%s"]/@href' % row
            url = response.xpath(expression).extract_first()
            if url:
                return scrapy.Request(url=url,
                                      callback=self.extract_docs,
                                      errback=lambda failure: self.request(row),
                                      dont_filter=True,
                                      meta={'row': row}
                                      )
        elif 'PartID' in response.url:
            return self.extract_docs(response)
        else:
            return self.create_item(row, '', '')

    def extract_docs(self, response):
        row = response.meta['row']
        pdf = response.xpath(
            '//*[@id="ctl00_Master_ContentPlaceHolder1_ContentPlaceHolderMain_HyperLinkCatalogPage"]/@href').extract_first()
        if pdf:
            name = response.xpath(
                '//*[@id="ctl00_Master_ContentPlaceHolder1_ContentPlaceHolderMain_HyperLinkCatalogPage"]/@title').extract_first()
            yield self.create_item(row, response.urljoin(pdf), name)
        info = response.xpath(
            '//*[@id="ctl00_Master_ContentPlaceHolder1_ContentPlaceHolderMain_HyperLinkInstructionSheet"]/@href').extract_first()
        if info:
            name = response.xpath(
                '//*[@id="ctl00_Master_ContentPlaceHolder1_ContentPlaceHolderMain_HyperLinkInstructionSheet"]/@title').extract_first()
            yield self.create_item(row, response.urljoin(info), name)
