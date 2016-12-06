import sys
import csv
import re
import os.path
from os import listdir
from os.path import isfile, join

csv.field_size_limit(sys.maxsize)

new_rows = []

###CHANGE DIRECTORY PATH AS REQUIRED###
save_path = 'C:\Users\serap\Desktop\inventtory_spider_respository_chris\inventtory_data_scraping\inventtory_data_scraping\inventtory_spiders\espacenet_china_Abstr-Claim-Descr\TXT_espacenet_china'

with open('CSV_espacenet_china\espacenet_china_1.csv', "rt") as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        if i == 0:
            header = row
        else:
            new_rows.append(row)
            

#########################
###PROCESS DATA FIELDS###
#########################

###ADJUST THE FIELDS LIST AS REQUIRED - fields must be from the EspacenetItem data model (see items.py file), and match exactly###
fields = ['document_url', 'key_identifier', 'patent_country', 'patent_country_code', 'patent_application_number', 'patent_number', 'patent_name', 'page_bookmark', 'inventors', 'applicants', 'classification_international', 'classification_cooperative', 'application_number', 'priority_numbers', 'abstract', 'patent_description', 'original_claims', 'claims_tree', 'cited_documents', 'citing_documents', 'INPADOC_legal_status', 'INPADOC_patent_family']

###WORK OUT NUMBER OF COPIES OF A DOCUMENT IN FOLDER###

if (os.listdir(save_path) == []) == True:

    for record in new_rows:
        patent_index = header.index('key_identifier')
        name_of_file = str(record[patent_index])+ "_1.txt"
        complete_name = os.path.join(save_path, name_of_file)
        f = open(complete_name,"w")
        print(name_of_file)
        for field in fields:
            field_index = header.index(field)
            entry = str(field) + ": " + "\n" + record[field_index] + "\n\n\n"
            f.write(entry)
        f.close()

else:

    for record in new_rows:
        patent_index = header.index('key_identifier')
        test_name = str(record[patent_index])
        only_files = [f for f in listdir(save_path) if isfile(join(save_path, f))]
        only_files = [re.match('([A-Z]{2}[0-9]+[0-9A-Z]{0,2}).*',e).group(1) for e in only_files]
        ###determine how many of a particular patent document there are in directory###
        num = only_files.count(test_name) + 1
        name_of_file = str(record[patent_index])+ '_' + str(num) + ".txt"
        complete_name = os.path.join(save_path, name_of_file)
        f = open(complete_name,"w")
        print(name_of_file)
        for field in fields:
            field_index = header.index(field)
            entry = str(field) + ": " + "\n" + record[field_index] + "\n\n\n"
            f.write(entry)
        f.close()


