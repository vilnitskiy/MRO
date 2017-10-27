import re
import pandas as pd
import csv

out = pd.read_csv("crawls/spiders/data/Crown_images_&_descr.csv", sep=',')
catalog_numbers = [str(item).strip() for item in list(out.catalog_number)]
descr = list(out.description)
ids = list(out.id)
sku = list(out.sku)
catalog_sku = dict(zip(catalog_numbers, sku))
catalog_ids = dict(zip(catalog_numbers, ids))
catalog_descr = dict(zip(catalog_numbers, descr))

out1 = pd.read_csv("result_crown.csv", sep=',')
catalog_numbers1 = list(out1.catalog_number)

diff = [item for item in catalog_numbers if item not in catalog_numbers1]

with open('diff_crown.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    spamwriter.writerow(['id', 'catalog_number', 'sku', 'description'])
    for item in diff:
    	spamwriter.writerow([catalog_ids[item], item, catalog_sku[item], catalog_descr[item]])

