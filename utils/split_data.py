import re
import pandas as pd
import csv

out = pd.read_csv("results/altramotion_results.csv", sep=',')
catalog_numbers = list(out.catalog_number)
ids = list(out.ids)
descr = list(out.description)
img_url = list(out.main_image)
add_descr = list(out.additional_description)
attributes = list(out.attributes)
catalog_ids = dict(zip(catalog_numbers, ids))
catalog_descr = dict(zip(catalog_numbers, descr))
catalog_img_url = dict(zip(catalog_numbers, img_url))
catalog_add_descr = dict(zip(catalog_numbers, add_descr))
catalog_attributes = dict(zip(catalog_numbers, attributes))


out1 = pd.read_csv("altramotion_with_brands.csv", sep=';')
catalog_numbers1 = list(out1.catalog_number)
ids1 = list(out1.id)
descr1 = list(out1.description)
img_url1 = list(out1.img_url)
add_descr1 = list(out1.add_descr)
attributes1 = list(out1.attributes)
catalog_ids1 = dict(zip(catalog_numbers1, ids1))
catalog_descr1 = dict(zip(catalog_numbers1, descr1))
catalog_img_url1 = dict(zip(catalog_numbers1, img_url1))
catalog_add_descr1 = dict(zip(catalog_numbers1, add_descr1))
catalog_attributes1 = dict(zip(catalog_numbers1, attributes1))



with open('results/altramotion_img.csv', 'wb') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
	spamwriter.writerow(['id', 'catalog_number', 'description'])
	for item in catalog_numbers:
		#if str(catalog_attributes1[item]) == 'nan':
		if catalog_img_url[item] != catalog_img_url1[item]:
			spamwriter.writerow([catalog_ids1[item], item, catalog_img_url[item]])

