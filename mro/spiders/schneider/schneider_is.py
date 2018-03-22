# -*- coding: utf-8 -*-
import json
import re
import pandas as pd
import scrapy
from mro.BaseSpiders.base_spiders import BaseMroSpider
from mro.items import UniversalItem



class Schneider(BaseMroSpider):
    name = "schneider_is"
    path_to_data = 'mro/spiders/csv_data/schneider/schneider_instruction_sheet.csv'
    separator = ','
    search_url = '{}'

    def start_requests(self):
        for row in self.catalog:
            yield scrapy.Request(url=self.search_url.format(self.catalog_instruction_sheet[row]),
                                 callback=self.parse_item,
                                 cookies=self.base_cookies,
                                 meta={'row': row}
                                 )

    def parse_item(self, response):
        filename = response.meta['row'].strip() + '.pdf'
        path = '/home/andrey_g/mro/schneider/instruction_sheet/' + filename
        with open(path, 'wb') as file:
            file.write(response.body)
