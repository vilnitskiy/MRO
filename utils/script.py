import re
import pandas as pd
import csv


f = open('DOC#2052637.txt', 'r')
data = f.read()
f.close()

GP1 = 0.00
GP2 = 0.00
freight = 0.00
ExtPrice = 0.00
items_count = 0


item_list = data.split('****************************************************************************************************************************************************')[:-1]

for item in item_list:
	item = item.split('Order #')[1]
	freight += float(re.findall(r'Freight :\s+([\d\.]+)\s+Handling', item)[0])
	ExtPriceList = re.findall(r'\s+[ -]\d+\.\d+\s+[ -]\d+\.\d+\s+[ -]\d+\.\d+\s+([ -]\d+\.\d+)\s+[ -]\d+\.\d+\s+[ -]\d+\.\d+\s', item)
	GP1List = re.findall(r'\s+[ -]\d+\.\d+\s+[ -]\d+\.\d+\s+[ -]\d+\.\d+\s+[ -]\d+\.\d+\s+([ -]\d+\.\d)+\s+[ -]\d+\.\d+\s', item)
	GP2List = re.findall(r'\s+[ -]\d+\.\d+\s+[ -]\d+\.\d+\s+[ -]\d+\.\d+\s+[ -]\d+\.\d+\s+[ -]\d+\.\d+\s+([ -]\d+\.\d)+\s', item)
	QuantityList = re.findall(r'[A-Z]\s{2,}(\d+)[a-zA-Z]{2}\s{3}[A-Z]\s+', item)
	for item in ExtPriceList:
		ExtPrice += float(item)
	for item in GP1List:
		GP1 += float(item)
	for item in GP2List:
		GP2 += float(item)
	items_count += len(ExtPriceList) 
	print QuantityList
GP2 = GP2/items_count


order_count = len(item_list)




