import re
import pandas as pd
import csv
'''
out = pd.read_csv("Crown_images_&_descr.csv", sep=',')
ids = [str(item).strip() for item in list(out.id)]
descr = list(out.description)
catalog_descr = dict(zip(ids, descr))

'''
out1 = pd.read_csv("mro/results/timken/timken_img.csv", sep=',')
catalog_numbers = [str(item) for item in list(out1.catalog_number)]
ids1 = [str(item) for item in list(out1.id)]

img = list(out1.img)
id_catalog = dict(zip(ids1, catalog_numbers))
id_img = dict(zip(ids1, img))



with open('timken_img_true.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    spamwriter.writerow(['id','catalog_number', 'img'])
    for item in ids1:
    	spamwriter.writerow([item, id_catalog[item], id_img[item]])

