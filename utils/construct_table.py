# -*- coding: utf-8 -*-
import lxml.html
import lxml.html.clean as clean
import re
import pandas as pd
import csv


f = open('test.html', 'r')
table = f.read()
f.close()

html = lxml.html.fromstring(table)
safe_attrs = clean.defs.safe_attrs
cleaner = clean.Cleaner(safe_attrs_only=True, safe_attrs=frozenset())
cleansed = cleaner.clean_html(html)
'''
table = re.sub(r'<table .+>', '<table>', table)
table = re.sub(r'<td .+>""', '<td>', table)

table = table.replace(' ', '')
table = table.replace('</td>\n\n<td>', '</td></tr><tr><td>')
table = table.replace('\n', '')

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



f = open('test1.html', 'w')
f.write(lxml.html.tostring(cleansed))
f.close()

