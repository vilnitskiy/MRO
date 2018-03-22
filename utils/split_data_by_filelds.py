import re
import pandas as pd
import csv

out = pd.read_csv("result_cooperindustries.csv", sep=',')
catalog_numbers = list(out.catalog_number)
ids = list(out.id)
img = list(out.img)
add_descr = list(out.add_descr)
attributes = list(out.attributes)

catalog_ids = dict(zip(catalog_numbers, ids))
catalog_img = dict(zip(catalog_numbers, img))
catalog_attributes = dict(zip(catalog_numbers, attributes))
catalog_add_descr = dict(zip(catalog_numbers, add_descr))


with open('mro/results/cooperindustries/cooperindustries_add_descr.csv', 'wb') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
	spamwriter.writerow(['id', 'catalog_number', 'add_descr'])
	for item in catalog_numbers:
		if str(catalog_add_descr[item]) != "nan":
			spamwriter.writerow([catalog_ids[item], 
				item,
				catalog_add_descr[item]
				])

