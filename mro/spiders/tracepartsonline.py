# -*- coding: utf-8 -*-
import json
import re
import urllib
import urllib2
import zipfile

import pandas as pd
import scrapy
from mro.items import UniversalItem

out = pd.read_csv("spiders/csv_data/tracepartsonline/tracepartsonline_others_pdf.csv", sep=',')
catalog = [str(item).strip() for item in list(out.catalog_number)]
ids = list(out.id)
catalog_ids = dict(zip(catalog, ids))

root = 'new/'


class Mcr(scrapy.Spider):
    name = "tracepartsonline"
    login_page = ''

    cookies = {
        'BROWSERGUID': 'e78b5ef0-1747-4ab9-9d7f-b308b7de22ca',
        'LB_SRV': 'server137',
        'ProdCfgPageViewStates': '%7b%22prodCfg_1%22%3a%7b%22type%22%3a1%2c%22scrolling%22%3a%7b%22top%22%3a-1%2c%22left%22%3a-1%7d%2c%22filtering%22%3a%7b%22state%22%3a-2%7d%2c%22sorting%22%3a%7b%22columnName%22%3a%22%22%2c%22descending%22%3afalse%7d%7d%7d',
    }

    def start_requests(self):
        return [scrapy.Request(url=self.login_page, cookies=self.cookies, callback=self.login)]

    def login(self, response):
        print response.body
        key = re.findall(r'/\(S\(([a-z0-9]+)\)\)/', response.url)[0]
        url = 'https://www.tracepartsonline.net/(S(' + key + '))/PartDetails.aspx?DetailLevels=2&CFSUB=1&CF=68&ExportCADModel=1&VwAutoRefresh=1&Vw3DManualRefreshDone=0&VwMode=3DWebGL&3DVwMode=3DWebGL&WebSite=GLOBALV3&Lang=en&Class=SKF&ClsID=%2FF_SKF%2FF_SKF004%2FF_SKF004003%2FF_SKF004003001%2F&ManId=SKF&sid=1&PartId=10-20012017-072320&PartTab=0&pageScrollTopPosition=&ProdCfgPageMode=1&ProdCfgPreviousViewMode=2&ProdCfgCurrentViewMode=2&ProdCfgSelectionPath=278%7C278%7C278%7C278%7C278%7C278%7C278%7C278%7C278%7C278%7C&ProdCfgVersion=1.0.5&ProdCfgTargetParametersGroup=1&ProdCfgTargetParameter=&ProdCfgTargetParameterSelectorOrValue=&ProdCfgPageViewStatesId=7F8820431B1040E286EB9CAA728F4E12&nbItemsReturned=29&SendComment=0&CommentWriter='
        return [
            scrapy.Request(url=url, cookies=self.cookies, callback=self.login2, dont_filter=True, meta={'key': key})]

    def login2(self, response):
        key = response.meta['key']
        for row in catalog:
            yield self.request(row, key)

    def request(self, row, key):
        url = 'https://www.tracepartsonline.net/(S(' + key + '))/content.aspx?SKeywords=' + urllib.quote_plus(
            row) + '&SDomain=1&st=4&sa=0&Class=SKF&clsid=%2fF_SKF%2f&ttl=SKF'
        return scrapy.Request(url=url,
                              callback=self.parse_item1,
                              errback=lambda failure: self.request(row, key),
                              dont_filter=True,
                              cookies=self.cookies,
                              meta={'row': row, 'key': key}
                              )

    def parse_item1(self, response):
        key = response.meta['key']
        row = response.meta['row']
        expression = '//span[text()="{}"]/../@href'.format(row)
        url = response.xpath(expression).extract_first()
        return scrapy.Request(url=response.urljoin(url),
                              callback=self.parse_item2,
                              errback=lambda failure: self.request(row, key),
                              dont_filter=True,
                              meta={'row': row},
                              cookies=self.cookies,
                              )

    def parse_item2(self, response):
        print response.url
        row = response.meta['row']
        sid = re.findall(r'var GloSelectionId = (\d+);', response.body)[0]
        key = re.findall(r'/\(S\(([a-z0-9]+)\)\)/', response.url)[0]
        formdata = dict(CommandName='DirectDownloadingCommand', sid=sid, CF='68', ClientType='0', ExportCADModel='1')
        url = 'https://www.tracepartsonline.net/(S(' + key + '))/rpc/AddToDownloadsList.aspx'
        return scrapy.FormRequest(url=url,
                                  callback=self.parse_item3,
                                  errback=lambda failure: self.request(row, key),
                                  dont_filter=True,
                                  meta={'row': row, 'key': key},
                                  cookies=self.cookies,
                                  formdata=formdata
                                  )

    def parse_item3(self, response):
        row = response.meta['row']
        key = response.meta['key']
        data = json.loads(response.body)
        url = 'https://www.tracepartsonline.net/(S(' + key + '))/rpc/GetDownloadsStatus.aspx?CommandName=DirectDownloadingCommand&ClientType=0&queueId=' + \
              data['results']
        return scrapy.Request(url=url,
                              callback=self.parse_item4,
                              errback=lambda failure: self.request(row, key),
                              dont_filter=True,
                              meta={'row': row},
                              cookies=self.cookies,
                              )

    def parse_item4(self, response):
        row = response.meta['row']
        url = re.findall(r"location.href='(.+)\'", response.body)[0].replace('\\', '')
        print url
        req = urllib2.Request(url)
        req.add_header("Cookie", 'BROWSERGUID=e78b5ef0-1747-4ab9-9d7f-b308b7de22ca; LB_SRV=server137')
        resp = urllib2.urlopen(req)
        name = '%s.zip' % row.replace('/', '_')
        f = open(root + name, 'wb')
        f.write(resp.read())
        f.close()
        if not zipfile.is_zipfile(root + name):
            item = UniversalItem()
            item['ids'] = catalog_ids[row]
            item[catalog_number] = row
            return item
