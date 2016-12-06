import sys
import re
import textwrap
import os.path

new_rows = []

save_path = 'C:\Users\serap\Desktop\inventtory_spider_respository_chris\inventtory_data_scraping\inventtory_data_scraping\inventtory_spiders\\'

with open('format_data_ESPACENET.py') as f_old:
    reader = f_old.readlines()
    for i, row in enumerate(reader):
        new_rows.append(row)

#################
###EDIT SCRIPT###
#################

find1 = re.match('(.*?=\s*)?\'C:\\.*',new_rows[12]).group(1)
find2 = re.match('with\s*open\(\'(.*?)\'.*',new_rows[15]).group(1)
#FILE PATH - new_rows[12]
new_rows[12] = find1 + '\'' + 'TEXT FOLDER' + '\''
#FILE NAME - new_rows[15]   
new_rows[15] = new_rows[15].replace(find2, 'ENTER NAME OF FILE HERE!')
name_of_file = "convert_uspto_applicant.py"
complete_name = os.path.join(save_path, name_of_file)
f_new = open(complete_name,"w")
for i, line in enumerate(new_rows):
    print(line)
    f_new.write(line)
f_new.close()
