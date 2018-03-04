# -*- coding: utf-8 -*-
import json
import re
import pandas as pd
import scrapy
from mro.BaseSpiders.base_spiders import BaseMroSpider
from mro.items import UniversalItem



class Baldor(BaseMroSpider):
    name = "baldor_cads_new"
    path_to_data = 'mro/spiders/csv_data/Baldor/baldor_2d_next.csv'
    separator = ','
    url_2d = 'http://www.baldor.com/api/products/cadfile/DXF2D-AUTOCAD%20VERSION%202013/{}/{}'
    url_dxf_3d = 'http://www.baldor.com/api/products/cadfile/DXF3D-AUTOCAD%20VERSION%202013/{}/{}'
    url_iges_3d = 'http://www.baldor.com/api/products/cadfile/IGES/{}/{}'

    def start_requests(self):
        for catalog in self.catalog:
            meta = {'catalog': catalog}
            yield scrapy.Request(url=self.url_2d.format(catalog, catalog),
                     callback=self.parse_item_2d,
                     meta=meta
                     )
            '''
            yield scrapy.Request(url=self.url_dxf_3d.format(catalog, catalog),
                     callback=self.parse_item_3d,
                     meta=meta
                     )
            '''

    def parse_item_2d(self, response):
        url = response.xpath('./text()').extract_first()
        if url:
            return scrapy.Request(url=url,
                     callback=self.download_cad,
                     meta={'catalog': response.meta['catalog'],
                            'type_cad': '2d'
                            }
                     )

    def parse_item_3d(self, response):
        url = response.xpath('./text()').extract_first()
        catalog = response.meta['catalog']
        if url:
            return scrapy.Request(url=url,
                     callback=self.download_cad,
                     meta={'catalog': catalog,
                            'type_cad': '3d'
                            }
                     )
        return scrapy.Request(url=self.url_iges_3d.format(catalog, catalog),
                     callback=self.parse_item_3d,
                     meta=response.meta
                     )

    def download_cad(self, response):
        filename = response.meta['catalog'].replace('/', '_').strip() + '.zip'
        path = 'mro/results/baldor/cads/' + response.meta['type_cad'] + '_next/' + filename
        with open(path, 'wb') as file:
            file.write(response.body)
