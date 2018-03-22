import os, shutil, csv
import pandas as pd

path = "results/Reelcraft/pdf_cad/"
files = os.listdir(path)


out = pd.read_csv("spiders/csv_data/Reelcraft/Export_for_products_product.csv", sep=',')
catalog_numbers = [str(item).strip() for item in list(out.catalog_number)]
ids = list(out.id)
catalog_ids = dict(zip(catalog_numbers, ids))


with open('results/reelcraft_pdf_next.csv', 'wb') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
	spamwriter.writerow(['id', 'catalog_number', 'pdf'])
	for f in files:
		if '.pdf' in f:
			item = f.replace('_', '/').replace('.pdf', '').strip()
			link = 'https://mro-host.herokuapp.com/file_download/?name=reelcraft_' + f
			spamwriter.writerow([catalog_ids[item], item, link])
	    	src = path+f
	    	dst = moveto+f
	    	shutil.move(src,dst)