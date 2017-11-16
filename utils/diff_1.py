import re
import pandas as pd
import csv

out = pd.read_csv("spiders/csv_data/Martin/martin.csv", sep=',')
catalog_numbers = [str(item).strip() for item in list(out.catalog_number)]
ids = list(out.id)
attributes = list(out.attributes)
catalog_ids = dict(zip(catalog_numbers, ids))
catalog_attributes = dict(zip(catalog_numbers, attributes))

out1 = pd.read_csv("results/Martin/martin_attributes.csv", sep=',')
catalog_numbers1 = list(out1.catalog_number)

diff = [item for item in catalog_numbers if item not in catalog_numbers1]

with open('martin_next.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    spamwriter.writerow(['id', 'catalog_number', 'attributes'])
    for item in diff:
    	spamwriter.writerow([catalog_ids[item], item, catalog_attributes[item]])

