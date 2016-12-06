# inventtory_data_scraping
data project


# BASIC SCRAPY OPERATION NOTES


##step 1 
[a] Open edit_settings.py in python idle, and edit steps 1 and 2 of the edit_settings.py files accordingly
[b] Run edit_settings.py in python idle by going to *run > run module*

##step 2 
[a] Open up terminal in Scrapy Project directory

##step 3 
[a] enter "scrapy crawl SPIDER_NAME" - replacing SPIDER_NAME with name of spider running

##step 4 
[a] When spider has finished crawling, run the conversion script, which can be found in the outermost spider folder
- i.e. for the espacenet_china spider, with Abstr-Claim-Descr data fields this would be in a folder called 
espacenet_china_Abstr-Claim-Descr
[b] Check the data fields in the fields list are consistent with choice of fields. i.e. for a USPTO/Abstr-Claim-Descr selection, the list 
should be *fields = ['document_url', 'key_identifier','abstract','patent_claims','patent_description']*
