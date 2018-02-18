import re
import pandas as pd
import csv

out = pd.read_csv("metropac_result_full.csv", sep=',')
catalog_numbers = map(str, out.catalog_number)


out1 = pd.read_csv("Product_2018-2-4 (1).csv", sep=',')
catalog_numbers1 = map(str, out1.catalog_number)
ids = map(str, out1.id)
catalog_id = dict(zip(catalog_numbers1, ids))

with open('metropac_next_items.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    spamwriter.writerow(['id','catalog_number'])
    for item in catalog_numbers1:
    	if item not in catalog_numbers:
    		spamwriter.writerow([catalog_id[item], item])

