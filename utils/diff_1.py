import re
import pandas as pd
import csv

out = pd.read_csv("mro/spiders/csv_data/Timken/timken_starter.csv", sep=',')
catalog_numbers = [str(item) for item in list(out.catalog_number)]
ids = list(out.id)
catalog_ids = dict(zip(catalog_numbers, ids))
'''
attributes = list(out.attributes)

catalog_attributes = dict(zip(catalog_numbers, attributes))
'''
out1 = pd.read_csv("mro/results/timken/timken_img.csv", sep=',')
catalog_numbers1 = [str(item) for item in list(out1.id)]
print catalog_numbers1

with open('timken_next.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    spamwriter.writerow(['id', 'catalog_number'])
    for item in set(catalog_numbers) - set(catalog_numbers1):

    	spamwriter.writerow([catalog_ids[item], item])

