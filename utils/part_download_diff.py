import os, shutil, csv
import pandas as pd

path = "/home/andrey_g/mro/schneider/instruction_sheet"
files = os.listdir(path)
print files[1]


out = pd.read_csv("mro/spiders/csv_data/schneider/schneider_instruction_sheet.csv", sep=',')
catalog_numbers = list(out.catalog_number)
ids = list(out.id)
catalog_ids = dict(zip(catalog_numbers, ids))


with open('mro/spiders/csv_data/schneider/instruction_sheet_next.csv', 'wb') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
	spamwriter.writerow(['id', 'catalog_number'])
	for f in catalog_numbers:
		if f + '.pdf' not in files:
			spamwriter.writerow([catalog_ids[f], f])