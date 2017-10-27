import re
import pandas as pd
import csv

out = pd.read_csv("result_grundfos.csv.csv", sep=',')
catalog_numbers = [str(item).strip() for item in list(out.catalog_number)]
image = list(out.image)
specifications = list(out.specifications)
description = list(out.description)
catalog_brand = dict(zip(catalog_numbers, brand))
catalog_ids = dict(zip(catalog_numbers, ids))
catalog_descr = dict(zip(catalog_numbers, descr))

diff = [item for item in catalog_numbers if str(catalog_descr[item]) == 'error1']

with open('regalpts_error1.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    spamwriter.writerow(['id', 'brand', 'catalog_number'])
    for item in diff:
    	spamwriter.writerow([catalog_ids[item], catalog_brand[item], item])

