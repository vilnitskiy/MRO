# -*- coding: utf-8 -*-

import re
import pandas as pd
import csv
from scrapy.selector import Selector
import lxml.html
import lxml.html.clean as clean

out = pd.read_csv("results/Martin/martin_attributes.csv", sep=',')
catalog_numbers = list(out.catalog_number)
ids = list(out.ids)
attributes = list(out.attributes)
catalog_ids = dict(zip(catalog_numbers, ids))
catalog_attributes = dict(zip(catalog_numbers, attributes))

def remove_html_attributes(string):
    html = lxml.html.fromstring(string)
    safe_attrs = clean.defs.safe_attrs
    cleaner = clean.Cleaner(safe_attrs_only=True, safe_attrs=frozenset())
    cleansed = cleaner.clean_html(html)
    string = lxml.html.tostring(cleansed)
    return re.sub(r'&#\d+;', '', string)

def custom_extractor(response, expression):
    data = response.xpath(expression).extract_first()
    return data if data else ' '

with open('results/Martin/martin_attributes_new.csv', 'wb') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
	spamwriter.writerow(['id', 'catalog_number', 'attributes'])
	for item in catalog_numbers:
		if str(catalog_attributes[item]) != 'nan':
			attr = ''
			html = remove_html_attributes(catalog_attributes[item])
			html = html.replace('<span>', '').replace('</span>', '')
			content = Selector(text=html)
			for tr in content.xpath('//table/tr'):
				attr += tr.xpath('./td[1]/text()').extract_first()+':'+custom_extractor(tr, './td[2]/text()') +"|"
			spamwriter.writerow([catalog_ids[item], item, attr[:-1]])



