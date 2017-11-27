import os
import zipfile
import pandas as pd
import csv

path = 'results/Reelcraft/dxf_cad/'
files = os.listdir(path)

for file in files:
	if not zipfile.is_zipfile(path + file):
		print file
		#os.remove(path + file)