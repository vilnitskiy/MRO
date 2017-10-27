# -*- coding: utf-8 -*-
import re
import pandas as pd
import csv


f = open('crawls/results/result_crown.csv', 'r')
table = f.read()
f.close()
'''
table = re.sub(r'<div class=""row"">(\n|\s)+<div class=""col-md-6 col-sm-12"">(\n|\s)+<dl class=""dl-horizontal"">', '<table>', table)
table = re.sub(r'</dl>(\n|\s)+</div>(\n|\s)+<div class=""col-md-6 col-sm-12 left-column"">(\n|\s)+<dl class=""dl-horizontal"">', '', table)
table = re.sub(r'</dl>(\n|\s)+</div>(\n|\s)+</div>(\n|\s)+<!-- SPC Attributes -->(\n|\s)+</div>', '</table>', table)
table = re.sub(r'</dt>(\n|\s)+<dd>', '</td><td>', table)
table = table.replace('<dt>', '<tr><td>')
table = table.replace('</dd>', '</td></tr>')

table = table.replace('<div class=""section detail-table product-overview"">', '<table>')
table = re.sub(r'</div>(\n|\s)+<div class=""col span_1_of_2"">', '', table)
table = table.replace('<div class=""col span_1_of_2"">', '')
table = re.sub(r'</div>(\n|\s)+</div>(\n|\s)+</div>(\n|\s)+</div>', '</div></table></div>', table)
table = re.sub(r'</div>(\n|\s)+<div>', '</tr><tr>', table)
table = table.replace('</div></table>', '</tr></table>')
table = table.replace('<div>', '<tr>')
table = table.replace('<span class=""label"">', '<td>').replace('<span class=""value"">', '<td>')
table = table.replace('</span>', '</td>')
'''



table = table.replace('′', "'").replace('™', '').replace('″', '"').replace('®','')


f = open('new_crown.csv', 'w')
f.write(table)
f.close()

