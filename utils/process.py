# -*- coding: utf-8 -*-
import re
import scrapy
import pandas
from csv import DictReader
from datetime import datetime
from collections import Counter

# origin file
data = pandas.read_csv("/data/work/virtualenvs/scrapy/crawls/skf_seals_download.csv", sep=',')
catalog = list(data.catalog_number)
ids = list(data.ids)
file_name = list(data.file_name)
catalog_ids = dict(zip(catalog, ids))
catalog_id = dict(zip(catalog, ids))
catalog_file = dict(zip(catalog, file_name))

ids_list = []
catalog_numbers_list = []
file_names_list = []

for cat in catalog:
	if str(catalog_file[cat]) != 'nan':
		print str(catalog_file[cat])
		file_name = str(cat).replace('/', '_').replace('X', 'x')
		link = 'https://mro-host.herokuapp.com/file_download/?name=skf_seals_' + file_name + '.dxf'

		ids_list.append(catalog_id[cat])
		catalog_numbers_list.append(cat)
		file_names_list.append(link)

testdict = {'ids': ids_list, 'catalog_number': catalog_numbers_list, 'file_links': file_names_list}
df = pandas.DataFrame(testdict)
print df
df.to_csv("rkf_cad_links_final.csv", sep=',', encoding='utf-8')

# code to delete spicific duplicates
"""
for item in dup_list:
  #df = new_data.ix[(new_data['catalog'] == item) & (new_data['industry_crossover_numbers'] == 'blank value')]
  new_data = new_data.drop(new_data[(new_data.industry_crossover_numbers == 'blank value') & (new_data.catalog == item)].index)
new_data.to_csv('/data/toshiba/toshiba/toshiba/new_processed_file_9.csv')
"""