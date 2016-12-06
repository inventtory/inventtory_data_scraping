import sys
import csv
import os
import os.path
import re
from os import listdir
from os.path import isfile, join

file_path = 'C:\Users\serap\Desktop\inventtory_spider_respository_chris\inventtory_data_scraping\inventtory_data_scraping\inventtory_spiders\espacenet_applicant_Abstr-Claim-Descr\TXT_espacenet_applicant'

only_files = [f for f in listdir(file_path) if isfile(join(file_path, f))]

#determine duplicates
only_files = [re.match('([A-Z]{2}[0-9]+[0-9A-Z]{0,2}).*',e).group(1) for e in only_files]


try:
    len([name for name in os.listdir(csv_path) if os.path.isfile(os.path.join(csv_path, name))])
    num = len([name for name in os.listdir(csv_path) if os.path.isfile(os.path.join(csv_path, name))]) + 1
except:
    num = 1
