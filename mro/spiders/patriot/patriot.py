# -*- coding: utf-8 -*-
import urllib

import pandas as pd
import scrapy
from mro.items import UniversalItem

out = pd.read_csv("mro/spiders/csv_data/Patriot/patriot.csv", sep=',')
catalog = list(out.catalog_number)
ids = list(out.id)
catalog_ids = dict(zip(catalog, ids))


class Patriot(scrapy.Spider):
    name = "patriot"
    '''
    DOWNLOAD_DELAY = 2
    CONCURRENT_REQUESTS = 1
    '''

    def start_requests(self):
        for row in out['catalog_number']:
            url = 'https://www.patriot-supply.com/search_new.cfm?q=' + urllib.quote_plus(str(row).strip()) + '&button='
            yield scrapy.Request(url=url,
                                 callback=self.parse_item1,
                                 meta={'meta_row': row}
                                 )

    def empty_item(self, meta_row):
        item = PatriotItem()
        item['ids'] = catalog_ids[meta_row]
        item['catalog_number'] = str(meta_row).strip()
        item['descr'] = ''
        return item

    def parse_item1(self, response):
        url = response.xpath('//*[@id="leftcol"]/div[2]/ul/li[1]/form/div/h3/a/@href').extract_first()
        if url:
            url = response.urljoin(url)
            return scrapy.Request(url=url,
                                  callback=self.parse_item2,
                                  meta={'meta_row': response.meta['meta_row']}
                                  )
        else:
            return self.empty_item(response.meta['meta_row'])

    def parse_item2(self, response):
        meta_row = response.meta['meta_row']
        if str(meta_row).strip().lower() == response.xpath(
                '//*[@id="leftcol"]/div[2]/div[2]/ul/li[2]/strong/text()').extract_first().lower():
            url = response.xpath('//*[@id="desc_ifr"]/@src').extract_first()
            url = response.urljoin(url)
            return scrapy.Request(url=url,
                                  callback=self.parse_item3,
                                  meta={'meta_row': meta_row}
                                  )
        else:
            return self.empty_item(meta_row)

    def parse_item3(self, response):
        descr = response.xpath('/html/body/div').extract_first()
        item = UniversalItem()
        item['ids'] = catalog_ids[response.meta['meta_row']]
        item['catalog_number'] = str(response.meta['meta_row']).strip()
        item['descr'] = descr
        return item
