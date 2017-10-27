import os
import zipfile
import pandas as pd
import csv

out = pd.read_csv("Regal_Beloit_3D_CAD.csv", sep=',')
catalog_numbers = [str(item).strip() for item in list(out.catalog_number)]
ids = list(out.id)
brand = list(out.Brand)
catalog_brand = dict(zip(catalog_numbers, brand))
catalog_ids = dict(zip(catalog_numbers, ids))

path = 'regalpts_/part3'
files = os.listdir(path)
'''
catalog = []
for file in files:
	if not zipfile.is_zipfile(path + '/' + file):
		catalog.append(file.replace('_', '/').replace('.zip', ''))

with open('bad1.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    for item in catalog:
    	spamwriter.writerow([item])
'''
with open('regalpts_/regalpts_links3.csv', 'wb') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
	spamwriter.writerow(['id', 'catalog_number', 'brand', 'cad'])
	for file in files:
		f=zipfile.ZipFile(path +'/' + file, 'r')
		filename = f.namelist()[0]
		print filename
		item = file.replace('_', '/').replace('.zip', '').strip()
		link = 'https://mro-host.herokuapp.com/file_download/?name=regalpts_beloit_' + filename
		spamwriter.writerow([catalog_ids[item], item, catalog_brand[item], link])
		f.extractall('regalpts_/unzip1')
		f.close()