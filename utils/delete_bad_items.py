import re
import pandas as pd
import csv

out = pd.read_csv("regalpts_/result_regalpts_original.csv", sep=',')
catalog_numbers = list(out.catalog_number)
brand = list(out.brand)
ids = list(out.ids)
descr = list(out.cad)
catalog_brand = dict(zip(catalog_numbers, brand))
catalog_ids = dict(zip(catalog_numbers, ids))
catalog_descr = dict(zip(catalog_numbers, descr))

with open('regalpts_/regalpts_without_errror1.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    spamwriter.writerow(['id', 'catalog_number', 'brand', 'cad'])
    for item in catalog_numbers:
    	if str(catalog_descr[item]) != 'error1':
    		spamwriter.writerow([catalog_ids[item], item, catalog_brand[item], catalog_descr[item]])

