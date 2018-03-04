import re
import pandas as pd
import csv

out = pd.read_csv("mro/results/baldor/baldor2d.csv", sep=',')
catalog_numbers = [str(i) for i in set(list(out.catalog_number))]

print len(catalog_numbers)

out1 = pd.read_csv("Product_2018-2-15 (1).csv", sep=',')
catalog_numbers1 = [str(i) for i in set(list(out1.catalog_number))]
ids = map(str, out1.id)
catalog_id = dict(zip(catalog_numbers1, ids))

with open('baldor_2d_next.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    spamwriter.writerow(['id','catalog_number'])
    for item in catalog_numbers1:
    	if item not in catalog_numbers:
    		spamwriter.writerow([catalog_id[item], item])

