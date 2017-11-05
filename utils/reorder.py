import csv

with open('/home/ilnitskiy/work/MRO/mro/results/carlislebelts1.csv', 'r') as infile, \
        open('/home/ilnitskiy/work/MRO/mro/results/carlislebelts_reordered.csv', 'a') as outfile:
    fieldnames = ['ids', 'catalog_number', 'description', 'image', 'brochure', 'product_specs', 'additional_description']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in csv.DictReader(infile):
        # writes the reordered rows to the new file
        writer.writerow(row)
