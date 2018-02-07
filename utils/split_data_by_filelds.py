import re
import pandas as pd
import csv

out = pd.read_csv("mro/Export_for_products_product.csv", sep=',')
catalog_numbers = list(out.catalog_number)
ids = list(out.id)
description = list(out.description)
main_image = list(out.main_image)
additional_description = list(out.additional_description)
Brand = list(out.Brand)
attributes = list(out.attributes)
catalog_ids = dict(zip(catalog_numbers, ids))
catalog_description = dict(zip(catalog_numbers, description))
catalog_main_image = dict(zip(catalog_numbers, main_image))
catalog_additional_description = dict(zip(catalog_numbers, additional_description))
catalog_Brand = dict(zip(catalog_numbers, Brand))
catalog_attributes = dict(zip(catalog_numbers, attributes))


['U.S.Tsubaki', 'Pyramex', 'Remco Products', 'Zero-Max']

with open('mro/Remco Products.csv', 'wb') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
	spamwriter.writerow(['id', 'catalog_number', 'description', 'main_image', 'additional_description', 'attributes', 'Brand'])
	for item in catalog_numbers:
		if catalog_Brand[item] == "Remco Products":
			spamwriter.writerow([catalog_ids[item], 
				item, 
				catalog_description[item], 
				catalog_main_image[item], 
				catalog_additional_description[item],
				catalog_attributes[item],
				catalog_Brand[item], 
				])

