import csv

with open('result_bostongear.csv', 'r') as infile, \
        open('bostongear.csv', 'a') as outfile:
        # documents	catalog_number	image	ids	additional_description	code	name
    fieldnames = ['ids', 'catalog_number', 'code', 'image', 'documents', 'name', 'additional_description']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in csv.DictReader(infile):
        writer.writerow(row)
