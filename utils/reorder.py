import csv

with open('mro/results/timken/timken_next_img.csv', 'r') as infile, \
        open('mro/results/timken/timken_next_img_r.csv', 'a') as outfile:
        # documents	catalog_number	image	ids	additional_description	code	name
    fieldnames = ['id', 'catalog_number', 'img']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in csv.DictReader(infile):
        writer.writerow(row)
