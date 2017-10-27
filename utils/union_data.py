import re
import pandas as pd
import csv

out = pd.read_csv("/data/work/virtualenvs/scrapy/crawls/weg_result/result_weg.csv", sep=',')
catalog_numbers = list(out.catalog_number)
ids = list(out.id)
descr = list(out.descr)
img_url = list(out.img_url)
add_descr = list(out.add_descr)
catalog_ids = dict(zip(catalog_numbers, ids))
catalog_descr = dict(zip(catalog_numbers, descr))
catalog_img_url = dict(zip(catalog_numbers, img_url))
catalog_add_descr = dict(zip(catalog_numbers, add_descr))

out1 = pd.read_csv("/data/work/virtualenvs/scrapy/crawls/weg11.csv", sep=',')
catalog_numbers1 = list(out1.catalog_number)
ids1 = list(out1.ids)
descr1 = list(out1.descr)
img_url1 = list(out1.img_url)
add_descr1 = list(out1.add_descr)
catalog_ids1 = dict(zip(catalog_numbers1, ids1))
catalog_descr1 = dict(zip(catalog_numbers1, descr1))
catalog_img_url1 = dict(zip(catalog_numbers1, img_url1))
catalog_add_descr1 = dict(zip(catalog_numbers1, add_descr1))



with open('union.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    spamwriter.writerow(['id', 'catalog_number', 'img_url', 'add_descr', 'descr'])
    for item in catalog_numbers:
    	if str(catalog_descr[item]) != 'nan':
    		spamwriter.writerow([catalog_ids[item], item, catalog_img_url[item], catalog_add_descr[item], catalog_descr[item]])
    	elif str(catalog_descr1[item]) != 'nan':
    		spamwriter.writerow([catalog_ids[item], item, catalog_img_url1[item], catalog_add_descr1[item], catalog_descr1[item]])
    	else:
    		spamwriter.writerow([catalog_ids[item], item, '', '', ''])


