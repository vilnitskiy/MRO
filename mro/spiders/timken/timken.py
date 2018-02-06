# -*- coding: utf-8 -*-
import json
import re
import pandas as pd
import scrapy
from mro.BaseSpiders.base_spiders import BaseMroSpider
from mro.items import UniversalItem



class Martin(BaseMroSpider):
    name = "timken"
    search_url = 'http://cad.timken.com/keyword/all-product-types?key=all&&keyword={}&SchType=2'
    path_to_data = 'mro/spiders/csv_data/Timken/timken_img_final.csv'
    separator = ','
    '''
    fields = ['id','supplier_id','brand_id','list_price','cost','description',
    'category_id','weight','condition','is_obsolete','ship_time','freight_class']
    '''
    fields = ['id']
    attributes = ['Specifications', 'Dimensions', 'Basic Load Ratings', 'Abutment and Fillet Dimensions', 'Basic Load Ratings', 'Factors']


    def parse_item(self, response, catalog=None, links=None):
        if catalog is None:
            catalog = response.meta['row']
        if links is None and '/item/' not in response.url:
            links = [i for i in response.xpath('//*[@id="plp-search-results-list"]/div[4]/div/span[1]/a[1]/@href').extract() if '/item/' in i]
            if not links:
                expression = '//*[@id="plp-table-filter"]/tbody/tr/td/span/a[text()="{}" or text()="{}"]/@href'.format(catalog, catalog.lower())
                url = response.xpath(expression).extract_first()
                if url:
                    return scrapy.Request(url=response.urljoin(url), callback=lambda response: self.parse_item(response, catalog, links))
        else:
            pages_catalog = response.xpath('//*[@id="plp-product-title"]/h1/text()').extract_first().split(',')[0].split('Number ')[1].lower()
            if pages_catalog == catalog.lower():
                #img = response.xpath('//*[@id="largegallery"]/div[@class="ad-nav"]/div[@class="ad-thumbs"]/ul/li[1]/a/@href').extract_first()
                E = UniversalItem()
                for attr in self.attributes:
                    print attr
                    path = response.xpath('//h3[@data-id="#{}"]/../div/table/tbody/tr'.format(attr))
                    temp = ''
                    if path:
                        for i in path:
                            first_part = i.xpath('./td[1]/h2/strong/text()').extract_first() or i.xpath('./td[1]/strong/text()').extract_first()
                            temp += first_part + ':' + ' '.join(i.xpath('./td[2]/span/span[2]/span/text()').extract()) + '|'
                    E[attr] = temp[:-1] if temp else ''
                E['id'] = self.catalog_id[catalog]
                E['catalog_number'] = catalog
                return E 
                '''
                if img:
                    return {
                        'id': self.catalog_id[catalog],
                        'img' : response.urljoin(img),
                        'catalog_number': catalog,
                        
                        }
                '''
        if links:
            return scrapy.Request(url=response.urljoin(links.pop(0)), callback=lambda response: self.parse_item(response, catalog, links))

'''
'supplier_id': self.catalog_supplier_id[catalog],
'brand_id': self.catalog_brand_id[catalog],
'list_price': self.catalog_list_price[catalog],
'cost': self.catalog_cost[catalog],
'description': self.catalog_description[catalog],
'category_id': self.catalog_category_id[catalog],

'weight': self.catalog_weight[catalog],
'condition': self.catalog_condition[catalog],
'is_obsolete': self.catalog_is_obsolete[catalog],
'ship_time': self.catalog_ship_time[catalog],
'freight_class': self.catalog_freight_class[catalog],
'''