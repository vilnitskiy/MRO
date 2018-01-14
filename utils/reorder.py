import csv

with open('results/mfg_add_descr_new.csv', 'r') as infile, \
        open('results/mfg_add_descr_new_new.csv', 'a') as outfile:
        # documents	catalog_number	image	ids	additional_description	code	name
    fieldnames = ['id', 'catalog_number', 'add_descr']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in csv.DictReader(infile):
        writer.writerow(row)
