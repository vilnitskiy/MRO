import re
import pandas as pd
import csv

out = pd.read_csv("results/reelcraft_pdf_new.csv", sep=',')
catalog_numbers = list(out.catalog_number)
ids = list(out.ids)
pdf = list(out.pdf)
catalog_ids = dict(zip(catalog_numbers, ids))
catalog_pdf = dict(zip(catalog_numbers, pdf))

with open('results/Reelcraft/pdf_links.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    spamwriter.writerow(['id', 'catalog_number', 'pdf'])
    for item in catalog_numbers:
    	link = 'https://mro-host.herokuapp.com/file_download/?name=reelcraft_' + catalog_pdf[item]
    	spamwriter.writerow([catalog_ids[item], item, link])


