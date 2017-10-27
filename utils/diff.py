import re
import pandas as pd
import csv

out = pd.read_csv("Crown_images_&_descr.csv", sep=',')
ids = [str(item).strip() for item in list(out.id)]
descr = list(out.description)
catalog_descr = dict(zip(ids, descr))


out1 = pd.read_csv("result_crown.csv", sep=',')
catalog_numbers = [str(item).strip() for item in list(out1.catalog_number)]
ids1 = [str(item).strip() for item in list(out1.ids)]
sku = list(out1.sku)
url = list(out1.url)
img = list(out1.img)
additional_description = list(out1.additional_description)

id_sku = dict(zip(ids, sku))
id_catalog = dict(zip(ids, catalog_numbers))
id_url = dict(zip(ids, url))
id_img = dict(zip(ids, img))
id_additional_description = dict(zip(ids, additional_description))


with open('crown', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    spamwriter.writerow(['sku','name','img','url','description','ids','additional_description','catalog_number'])
    for item in ids1:
    	spamwriter.writerow([id_sku[item], 'Spec Sheet', id_img[item], id_url[item], catalog_descr[item], item, id_additional_description[item], id_catalog[item]])

