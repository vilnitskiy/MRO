import os
import zipfile
import pandas as pd
import csv

out = pd.read_csv("Product_2018-2-15 (1).csv", sep=',')
catalog_numbers = map(str, out.catalog_number)
catalog_ids = dict(zip(catalog_numbers, list(out.id)))

path = 'mro/results/baldor/cads/2d'
files = os.listdir(path)


with open('mro/results/baldor/baldor2d.csv', 'wb') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
	spamwriter.writerow(['id', 'catalog_number', 'cad', 'type'])
	for file in files:
		f=zipfile.ZipFile(path +'/' + file, 'r')
		filenames = f.namelist()[1:]
		if len(filenames) != 3:
			raise Exception
		print filenames
		catalog = file.replace('_', '/').replace('.zip', '').strip()
		items = iter(['front', 'right', 'top'])
		for item in filenames:
			link = 'https://mro-host.herokuapp.com/file_download/?name=baldor2d_' + item
			spamwriter.writerow([catalog_ids[catalog], catalog, link, next(items)])
		f.extractall('/home/andrey_g/mro/baldor2d')
		f.close()

'''
with open('mro/results/baldor/baldor2d.csv', 'wb') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
	spamwriter.writerow(['id', 'catalog_number', 'cad'])
	for file in files:
		f=zipfile.ZipFile(path +'/' + file, 'r')
		filename = f.namelist()[0]
		print filename
		item = file.replace('_', '/').replace('.zip', '').strip()
		link = 'https://mro-host.herokuapp.com/file_download/?name=baldor2d_' + filename
		spamwriter.writerow([catalog_ids[item], item, link])
		f.extractall('/home/andrey_g/mro/baldor2d')
		f.close()
'''