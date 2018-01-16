# -*- coding: utf-8 -*-
import pandas as pd
import scrapy
from mro.items import UniversalItem

out = pd.read_csv("mro/spiders/csv_data/Durhammfg/mfg.csv", sep=';')
catalog = [str(item).strip() for item in list(out.catalog_number)]
ids = list(out.id)
catalog_ids = dict(zip(catalog, ids))


class Weg(scrapy.Spider):
    name = "mfg"

    def start_requests(self):
        for row in catalog:
            url = 'http://www.durhammfg.com/search.html?searchterm=' + row
            yield scrapy.Request(url=url, 
                callback=self.parse_item, 
                meta={'row': row},
                dont_filter=True)


    def parse_item(self, response):
        if 'item' in response.url:
            row = response.meta['row']
            add_descr = response.xpath('//td[@class="item_desc"]/text()').extract()
            '''
            attr_table = response.xpath('//td[@class="item_desc"]/table[1]/tr')
            
            attr = ''
            if attr_table:
                for i in attr_table:
                    attr += i.xpath('./td[1]/b/text()').extract_first() + ':' + ' '.join(i.xpath('./td[2]/text()').extract()).replace('\n', ' ') + '|'
            '''
            item = UniversalItem()
            item['id'] = catalog_ids[row]
            item['catalog_number'] = row
            #item['attributes'] = attr[:-1]
            item['add_descr'] = ''.join(add_descr[1:]) if add_descr else ''
            return item


