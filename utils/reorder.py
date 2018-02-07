import csv


with open('./zero_attr.csv', 'r') as infile, \
        open('mro/results/zero/zero_attr.csv', 'a') as outfile:
        # documents	catalog_number	image	ids	additional_description	code	name
    fieldnames = ['id', 'catalog_number', 'attributes',]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in csv.DictReader(infile):
        writer.writerow(row)
