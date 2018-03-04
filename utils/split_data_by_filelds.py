import re
import pandas as pd
import csv

out = pd.read_csv("result_schneider.csv", sep=',')
catalog_numbers = list(out.catalog_number)
ids = list(out.id)
instruction_sheet = list(out.instruction_sheet)
product_datasheet = list(out.product_datasheet)

catalog_ids = dict(zip(catalog_numbers, ids))
catalog_instruction_sheet = dict(zip(catalog_numbers, instruction_sheet))
catalog_product_datasheet = dict(zip(catalog_numbers, product_datasheet))


with open('mro/results/schneider/schneider_product_datasheet.csv', 'wb') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
	spamwriter.writerow(['id', 'catalog_number', 'product_datasheet'])
	for item in catalog_numbers:
		if str(catalog_product_datasheet[item]) != "nan":
			spamwriter.writerow([catalog_ids[item], 
				item,
				catalog_product_datasheet[item][2:]
				])

