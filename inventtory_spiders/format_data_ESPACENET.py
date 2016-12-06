import sys
import csv
import os.path

csv.field_size_limit(sys.maxsize)

new_rows = []

###CHANGE DIRECTORY PATH AS REQUIRED###
save_path = 'C:\Users\serap\Documents\inventtory_data_scraping\inventtory_data_scraping\inventtory_spiders\DATA_OUTPUT2'


with open('espacenet_china_test1.csv', "rt") as f:
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

try:
    len([name for name in os.listdir(csv_path) if os.path.isfile(os.path.join(csv_path, name))])
    num = len([name for name in os.listdir(csv_path) if os.path.isfile(os.path.join(csv_path, name))]) + 1
except:
    num = 1

for record in new_rows:
    patent_index = header.index('key_identifier')
    #patent_index = header.index('patent_number')
    name_of_file = str(record[patent_index])+ ".txt"
    complete_name = os.path.join(save_path, name_of_file)
    #f = open(str(record[header.index('patent_number')])+".txt","w")
    f = open(complete_name,"w")
    print(record[patent_index])
    for field in fields:
        field_index = header.index(field)
        entry = str(field) + ": " + "\n" + record[field_index] + "\n\n\n"
        f.write(entry)
    f.close()


