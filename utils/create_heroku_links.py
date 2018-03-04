import os
import zipfile
import pandas as pd
import csv

out = pd.read_csv("Product_2018-2-15 (1) (2).csv", sep=',')
catalog_numbers = map(str, out.catalog_number)
catalog_ids = dict(zip(catalog_numbers, list(out.id)))

path = '/home/andrey_g/mro/schneider/dxf'
files = os.listdir(path)


with open('mro/results/schneider/schneiderdxf.csv', 'wb') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
	spamwriter.writerow(['id', 'catalog_number', 'cad'])
	for file in files:
		catalog = file.split('.dxf')[0]
		link = 'https://mro-host.herokuapp.com/file_download/?name=schneiderdxf_' + file
		spamwriter.writerow([catalog_ids[catalog], catalog, link])
