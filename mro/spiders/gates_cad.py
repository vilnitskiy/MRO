# -*- coding: utf-8 -*-
import shutil
import urllib
import urllib2

import pandas as pd
import scrapy

from mro.items import GatesItem

out = pd.read_csv("spiders/csv_data/Gates/gates.csv", sep=',')
catalog = list(out.catalog_number)
ids = list(out.id)
catalog_ids = dict(zip(catalog, ids))


class GatesCadCrawl(scrapy.Spider):
    name = "gates_cad"
    index = 0

    def start_requests(self):
        for row in out['catalog_number']:
            meta_row = row
            row = self.replace_symbols(str(row).strip())
            url = 'http://partview.gates.com/catalog3/cad?d=gates.pt&id=' + row + '&f=igs'
            proxy = 'http://108.59.14.208:13040/'
            self.index = 0
            yield self.request(url, meta_row, row, proxy)

    def request(self, url, meta_row, row, proxy):
        callback = lambda response: self.parse_item(response, meta_row, row, url)
        # errback = lambda failure: self.repeat(failure, url, meta_row, row)
        return scrapy.Request(url=url,
                              callback=callback,
                              # errback=errback,
                              meta={'proxy': proxy},
                              dont_filter=True)

    # def repeat(self, failure, url, meta_row, row):
    #     proxy = '108.59.14.203:13040'
    #     return self.request(url, meta_row, row, proxy)

    def replace_symbols(self, row):
        return row.replace('/', '_').replace('.', '-')

    def parse_item(self, response, meta_row, row, url):
        if 'restricted access' in response.xpath('//*').extract_first():
            print meta_row
            print 'restricted access'
            if self.index > 5:
                print 'the end'
                return
            proxy = 'http://108.59.14.203:13040/'
            self.index += 1
            return self.request(url, meta_row, row, proxy)
        else:
            item = GatesItem()
            item['ids'] = catalog_ids[meta_row]
            item['catalog_number'] = str(meta_row).strip()
            try:
                url = response.xpath('//*').re(r'"url":"(.+)","productID"')[0]
                print '--------'
                print url
                req = urllib2.Request('http:' + url)
                resp = urllib2.urlopen(req)
                file_name = '%s.zip' % urllib.quote_plus(str(meta_row).strip())
                with open('gates_downoad/' + file_name, 'wb') as file:
                    shutil.copyfileobj(resp.fp, file)
            except Exception:
                return
            else:
                item['cad'] = file_name
            return item
