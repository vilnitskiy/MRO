# -*- coding: utf-8 -*-
import json
import re
import pandas as pd
import scrapy
from mro.BaseSpiders.base_spiders import BaseMroSpider



class Martin(BaseMroSpider):
    name = "martin"
    search_url = 'http://products.remcoproducts.com/Search.aspx?Keyword={}'
    path_to_data = 'mro/spiders/csv_data/Remko/remko.csv'
    separator = ','
    fields = ['id', 'main_image', 'additional_description', 'attributes', 'description']


    def parse_item(self, response):
        row = response.meta['row']
