import re
import pandas as pd
import csv

out = pd.read_csv("./ustsubaki_result.csv", sep=',')
catalog_numbers = list(out.catalog_number)
ids = list(out.id)
specifications = list(out.specifications)
main_image = list(out.main_image)
chain_technical_data = list(out.chain_technical_data)
sprocket_diameters = list(out.sprocket_diameters)
locking_bolts = list(out.locking_bolts)
catalog_ids = dict(zip(catalog_numbers, ids))
catalog_specifications = dict(zip(catalog_numbers, specifications))
catalog_main_image = dict(zip(catalog_numbers, main_image))
catalog_chain_technical_data = dict(zip(catalog_numbers, chain_technical_data))
catalog_sprocket_diameters = dict(zip(catalog_numbers, sprocket_diameters))
catalog_locking_bolts = dict(zip(catalog_numbers, locking_bolts))


['U.S.Tsubaki', 'Pyramex', 'Remco Products', 'Zero-Max']

with open('mro/results/ustsubaki/ustsubaki_chain_technical_data.csv', 'wb') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
	spamwriter.writerow(['id', 'catalog_number', 'chain_technical_data'])
	for item in catalog_numbers:
		if str(catalog_chain_technical_data[item]) != "nan":
			spamwriter.writerow([catalog_ids[item], 
				item, 
				catalog_chain_technical_data[item], 
				])

