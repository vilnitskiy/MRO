import os
import zipfile
import pandas as pd
import csv

path = 'regalpts_download/'
files = os.listdir(path)

for file in files:
	if not zipfile.is_zipfile(path + file):
		os.remove(path + file)