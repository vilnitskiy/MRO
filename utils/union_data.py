import re
import pandas as pd
import csv

out = pd.read_csv("mro/Remco Products.csv", sep=',')
catalog_numbers = map(lambda x: str(x), list(out.catalog_number))
ids = list(out.id)
attributes = list(out.attributes)
img_url = list(out.main_image)
add_descr = list(out.additional_description)
catalog_ids = dict(zip(catalog_numbers, ids))
catalog_attributes = dict(zip(catalog_numbers, attributes))
catalog_img_url = dict(zip(catalog_numbers, img_url))
catalog_add_descr = dict(zip(catalog_numbers, add_descr))

out1 = pd.read_csv("remko_result.csv", sep=',')
catalog_numbers1 = map(lambda x: str(x), list(out1.catalog_number))
ids1 = list(out1.id)
attributes1 = list(out1.attributes)
img_url1 = list(out1.main_image)
add_descr1 = list(out1.additional_description)
catalog_ids1 = dict(zip(catalog_numbers1, ids))
catalog_attributes1 = dict(zip(catalog_numbers1, attributes1))
catalog_img_url1 = dict(zip(catalog_numbers1, img_url1))
catalog_add_descr1 = dict(zip(catalog_numbers1, add_descr1))



with open('remko_additional_description.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    spamwriter.writerow(['id', 'catalog_number', 'additional_description'])
    for item in catalog_numbers1:
    	if str(catalog_add_descr1[item]) != str(catalog_add_descr[item]):
    		spamwriter.writerow([catalog_ids[item], item, catalog_add_descr1[item]])


