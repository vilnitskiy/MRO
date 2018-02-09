# -*- coding: utf-8 -*-
import json
import re
import pandas as pd
import scrapy
from mro.BaseSpiders.base_spiders import BaseMroSpider
from mro.items import UniversalItem



class Martin(BaseMroSpider):
    name = "midlandmetal"
    search_url = 'https://midlandmetal.com/item_detail.php?item={}'
    path_to_data = 'mro/spiders/csv_data/midlandmetal/midlandmetal.csv'
    separator = ','
    exclude_fields = ['industry_crossover_numbers']


    def parse_item(self, response):
        catalog = response.meta['row']
        base_data = response.xpath('//th[text()="Industry Crossover Numbers"]/../..')
        industry_crossover_numbers = 'not found'
        if base_data:
            industry_crossover_numbers = base_data.extract_first() if len(base_data.xpath('./tr')) > 1 else 'blank value'
        return {
            'id': self.catalog_id[catalog],
            'catalog': catalog,
            'industry_crossover_numbers': industry_crossover_numbers
        }




