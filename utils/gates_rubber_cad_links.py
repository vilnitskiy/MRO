import pandas as pd
import csv

out = pd.read_csv("/data/work/virtualenvs/scrapy/crawls/gates_result/gates_full.csv", sep=',')
catalog_numbers = list(out.catalog_number)
ids = list(out.ids)
cad = list(out.cad)
catalog_ids = dict(zip(catalog_numbers, ids))
catalog_cad = dict(zip(catalog_numbers, cad))

with open('gates_rubber_result.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    spamwriter.writerow(['id', 'catalog_number', 'cad'])
    for item in catalog_numbers:
        if str(catalog_cad[item]) != 'nan':
            link = 'https://mro-host.herokuapp.com/file_download/?name=gates_rubber_' + str(item).replace('.', '_').replace('/','_') + '.dxf'
            spamwriter.writerow([catalog_ids[item], item, link])
