# -*- coding: utf-8 -*-
import json
import re
import pandas as pd
import scrapy
from mro.BaseSpiders.base_spiders import BaseMroSpider
from mro.items import UniversalItem



class Schneider(BaseMroSpider):
    name = "schneider"
    path_to_data = 'mro/spiders/csv_data/schneider/instruction_sheet_next.csv'
    separator = ','
    search_url = 'https://www.schneider-electric.us/en/product/{}'
    '''
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'CONCURRENT_REQUESTS': 2
    }
    '''

    def start_requests(self):
        for row in self.catalog:
            yield scrapy.Request(url=self.search_url.format(row),
                                 callback=self.parse_item,
                                 cookies=self.base_cookies,
                                 meta={'row': row}
                                 )

    def parse_item(self, response):
        catalog = response.meta['row']
        site_catalog = response.xpath('//h1[@class="pdp-product-info__id"]/text()').extract_first() or ''
        if catalog.lower() == site_catalog.strip().lower():
            #product_datasheet = response.xpath('//div[text()="Product Datasheet"]/../@href').extract_first() or ''
            instruction_sheet = response.xpath('//div[text()="Instruction Sheet"]/../@href').extract_first() or ''
            '''
            cads = response.xpath('//div[@class="docs-table__column-name hyphenate" and text()="CAD"]/../../div[@class="js-pdp-section-sortable docs-table__section-sortable"]/div/div')
            if cads:
                pdf = cads.xpath('./div[@class="docs-table__column-name hyphenate"]/a[contains(@href, ".pdf")]/@href').extract_first()
                dxf = cads.xpath('./div[@class="docs-table__column-name hyphenate"]/a[contains(@href, ".dxf")]/@href').extract_first()
                if pdf:
                    yield scrapy.Request(url=pdf,
                     callback=self.download_cad,
                     meta={'catalog': catalog,
                            'type_cad': 'pdf'
                            }
                     )
                if dxf:
                    yield scrapy.Request(url=dxf,
                     callback=self.download_cad,
                     meta={'catalog': catalog,
                            'type_cad': 'dxf'
                            }
                     )
            '''
            if instruction_sheet:
                yield scrapy.Request(url=instruction_sheet,
                     callback=self.download_cad,
                     meta={'catalog': catalog,
                            'type_cad': 'instruction_sheet'
                            }
                     )
            '''
            yield {
                'id': self.catalog_id[catalog],
                'catalog_number': catalog,
                'product_datasheet': product_datasheet,
                'instruction_sheet': instruction_sheet
            }
            '''
    def download_cad(self, response):
        type_cad = response.meta['type_cad']
        filename = response.meta['catalog'].strip() + '.' + 'pdf'
        path = '/home/andrey_g/mro/schneider/' + type_cad + '/' + filename
        with open(path, 'wb') as file:
            file.write(response.body)
