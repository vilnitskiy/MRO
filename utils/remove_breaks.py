# -*- coding: utf-8 -*-
import pandas

# ordering_number, item_code, description, add_descr, ids
data = pandas.read_csv("../mro/results/result_flexco_new.csv", sep=',')

ordering = list(data.ordering_number)
ids = list(data.ids)
item_codes = list(data.item_code)
additional_descriptions = list(data.add_descr)
descriptions = list(data.description)

ordering_ids = dict(zip(ordering, ids))
ordering_item_codes = dict(zip(ordering, item_codes))
ordering_additional_descriptions = dict(zip(ordering, additional_descriptions))
ordering_descriptions = dict(zip(ordering, descriptions))

ids_list = []
ordering_list = []
item_codes_list = []
additional_descriptions_list = []
descriptions_list = []

for ord in ordering:
    mystr = " ".join(ordering_additional_descriptions[ord].split())
    ids_list.append(ordering_ids[ord])
    ordering_list.append(ord)
    item_codes_list.append(ordering_item_codes[ord])
    descriptions_list.append(ordering_descriptions[ord])
    additional_descriptions_list.append(mystr)

data = {
    'ids': ids_list,
    'ordering_number': ordering_list,
    'item_code': item_codes_list,
    'additional_description': additional_descriptions_list,
    'description': descriptions_list,
}

df = pandas.DataFrame(data)
df.to_csv("../mro/results/result_flexco_without_linebreaks.csv", sep=',', index=False, encoding='utf-8')
