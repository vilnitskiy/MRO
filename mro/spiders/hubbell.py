# -*- coding: utf-8 -*-
import pandas
import scrapy
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector

from mro.items import HubellItem

out = pandas.read_csv("spiders/csv_data/Hubbell-wiring/test.csv", sep=',')
catalog = list(out.catalog_number)
ids = list(out.ids)
urls = list(out.url_page)
catalog_ids = dict(zip(catalog, ids))
catalog_url = dict(zip(catalog, urls))


class HubbellSpider(CrawlSpider):
    name = "hubbell"
    allowed_domains = ["hubbell-wiring.com"]
    items = []

    start_urls = ['http://www.hubbell-wiring.com/csi.aspx']

    def parse(self, response):
        viewstate = response.xpath('//input[@name="__VIEWSTATE"]/@value').extract()
        viewstategenerator = response.xpath('//input[@name="__VIEWSTATEGENERATOR"]/@value').extract()
        eventvalidation = response.xpath('//input[@name="__EVENTVALIDATION"]/@value').extract()
        for row in out['catalog_number']:
            url = 'http://www.hubbell-wiring.com/csi.aspx'

            formdata = {
                "__EVENTTARGET": "",
                "__EVENTARGUMENT": "",
                "__VIEWSTATE": viewstate,
                "__VIEWSTATEGENERATOR": viewstategenerator,
                "__EVENTVALIDATION": eventvalidation,
                "ctl00$search": "WEBSITE",
                "ctl00$SRCH": "",
                "ctl00_RadMenu1_ClientState": "",
                "ctl00_mastermain_RadTabStrip1_ClientState": '{"selectedIndexes":["0"],"logEntries":[],"scrollState":{}}',
                "ctl00$mastermain$Part": str(row),
                "ctl00$mastermain$Family": "",
                "ctl00$mastermain$Button1": "Search",
                "ctl00_mastermain_RadGrid1_ClientState": "",
                "ctl00_mastermain_RadMultiPage1_ClientState": "",
            }

            meta = {"catalog_number": row}

            yield scrapy.FormRequest(
                url=url,
                formdata=formdata,
                dont_filter=True,
                meta=meta,
                callback=self.parse_item
            )

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)

        catalog_number = response.request.meta['catalog_number']

        item = HubellItem()

        item['ids'] = catalog_ids[catalog_number]
        item['catalog_number'] = catalog_number
        item['url_page'] = catalog_url[catalog_number]
        if response.xpath('//a[@title="Product Drawing PDF"]/@href'):
            item['Product_Drawing_PDF'] = response.xpath('//a[@title="Product Drawing PDF"]/@href').extract()[0]
        else:
            item['Product_Drawing_PDF'] = ''

        if response.xpath('//a[@title="Product Drawing DWG"]/@href'):
            item['Product_Drawing_DWG'] = response.xpath('//a[@title="Product Drawing DWG"]/@href').extract()[0]
        else:
            item['Product_Drawing_DWG'] = ''

        if response.xpath('//a[@title="Installation Instructions"]/@href'):
            item['Installation_Instructions'] = \
            response.xpath('//a[@title="Installation Instructions"]/@href').extract()[0]
        else:
            item['Installation_Instructions'] = ''

        yield item
