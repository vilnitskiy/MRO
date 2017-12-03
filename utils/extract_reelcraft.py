import os
import zipfile
import pandas as pd
import csv

out = pd.read_csv("results/reelcraft_igs.csv", sep=',')
catalog_numbers = [str(item).strip() for item in list(out.catalog_number)]
ids = list(out.ids)
dxf = list(out.igs)
catalog_ids = dict(zip(catalog_numbers, ids))
dxf_catalog = dict(zip(catalog_numbers, dxf))

path = 'results/Reelcraft/igs_cad'
files = [item for item in os.listdir(path) if '.zip' in item]

to = 'results/Reelcraft/extract_igs'

with open('results/igs_links.csv', 'wb') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
	spamwriter.writerow(['id', 'catalog_number', 'dxf'])
	for row in catalog_numbers:
		if '.igs' not in dxf_catalog[row]:
			ii = True
			f=zipfile.ZipFile(path +'/' + dxf_catalog[row], 'r')
			for files in f.namelist():
				if 'tw' in files.split("/")[-1].lower():
					item = dxf_catalog[row].replace('_', '/').replace('.zip', '').strip()
					print item
					link = 'https://mro-host.herokuapp.com/file_download/?name=reelcraft_' + files.split("/")[-1]
					spamwriter.writerow([catalog_ids[row], row, link])
					data = f.read(files, to)
					myfile_path = os.path.join(to, files.split("/")[-1])
					myfile = open(myfile_path, "wb")
					myfile.write(data)
					myfile.close()
					ii = False
					break
			if ii:
				item = dxf_catalog[row].replace('_', '/').replace('.zip', '').strip()
				print item
				link = 'https://mro-host.herokuapp.com/file_download/?name=reelcraft_' + f.namelist()[0].split("/")[-1]
				spamwriter.writerow([catalog_ids[row], row, link])
				data = f.read(f.namelist()[0], to)
				myfile_path = os.path.join(to, f.namelist()[0].split("/")[-1])
				myfile = open(myfile_path, "wb")
				myfile.write(data)
				myfile.close()
				f.close()
		else:
			link = 'https://mro-host.herokuapp.com/file_download/?name=reelcraft_' + dxf_catalog[row]
			spamwriter.writerow([catalog_ids[row], row, link])