import csv


with open('./midlandmetal_result.csv', 'r') as infile, \
        open('mro/results/midlandmetal/midlandmetal.csv', 'a') as outfile:
        # documents	catalog_number	image	ids	additional_description	code	name
    fieldnames = ['id', 'catalog', 'industry_crossover_numbers']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in csv.DictReader(infile):
        writer.writerow(row)
