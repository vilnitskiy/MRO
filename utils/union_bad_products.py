import re
import pandas as pd
import csv

out = pd.read_csv("/data/work/virtualenvs/scrapy/crawls/weg11.csv", sep=',')
catalog_numbers = list(out.catalog_number)
ids = list(out.ids)
catalog_ids = dict(zip(catalog_numbers, ids))
out1 = pd.read_csv("/data/work/virtualenvs/scrapy/crawls/weg_huevie_products.csv", sep=',')
catalog_numbers1 = list(out1.catalog_number)
ids1 = list(out1.id)
catalog_ids = dict(zip(catalog_numbers1, ids1))




with open('weg11.csv', 'a') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    for item in catalog_numbers1:
    	spamwriter.writerow([catalog_ids[item], '', item, '', ''])

