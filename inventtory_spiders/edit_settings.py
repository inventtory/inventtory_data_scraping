import sys
import re
import textwrap
import os, os.path
import time


new_rows = []

############################
###ENTER SPIDER NAME HERE###      #-*-STEP 1-*-#
############################

spider_name = 'espacenet_china'

timestr = time.strftime("%Y%m%d-%H%M%S")

##################
###DATA OPTIONS###
##################

option_1 = 'Abstr-Claim-Descr'
option_2 = 'All-Fields'

#########################################################
###EDIT DIRECTORY PATHS TO MATCH YOUR LOCAL REPOSITORY###
#########################################################

save_path = 'C:\Users\serap\Desktop\inventtory_spider_respository_chris\inventtory_data_scraping\inventtory_data_scraping\inventtory_spiders\inventtory_spiders'
edit_path = 'C:\Users\serap\Desktop\inventtory_spider_respository_chris\inventtory_data_scraping\inventtory_data_scraping\inventtory_spiders'

#################################
###COMMENT OUT PATHS NOT USING###      #-*-STEP 2-*-#
#################################

log_path = edit_path + '\\' + spider_name + '_' + option_1 + '\\' + 'LOG_' + spider_name
#log_path = edit_path + '\\' + spider_name + '_' + option_2 + '\\' + 'LOG_' + spider_name


if not os.path.exists(log_path):
    os.makedirs(log_path)
else:
    log_path = log_path
    

try:
    len([name for name in os.listdir(log_path) if os.path.isfile(os.path.join(log_path, name))])
    num = len([name for name in os.listdir(log_path) if os.path.isfile(os.path.join(log_path, name))]) + 1
except:
    num = 1
    

with open(save_path + '\\' + 'settings.py') as f_old:
    reader = f_old.readlines()
    for i, row in enumerate(reader):
        new_rows.append(row)

#################
###EDIT SCRIPT###
#################
try:
    re.match('(.*?=\s*)(?:.*?)?(\n.*)',new_rows[102]).group(1)
    find1 = re.match('(.*?=\s*)(?:.*?)?(\n.*)',new_rows[102]).group(1)
except:
    print("need fixing!")
    
try:
    re.match('(.*?=\s*)(?:.*?)?(\n.*)',new_rows[102]).group(2)
    find2 = re.match('(.*?=\s*)(?:.*?)?(\n.*)',new_rows[102]).group(2)
except:
    print("need fixing!")
    

###########################
###DETERMINE FILE NUMBER###
###########################

new_rows[102] = find1 + '\'' + log_path +'\\' + spider_name + '_' + str(num) + '.log\'' + find2

name_of_file = "settings.py"
complete_name = os.path.join(save_path, name_of_file)
f_new = open(complete_name,"w")
for i, line in enumerate(new_rows):
    print(line)
    f_new.write(line)
f_new.close()
