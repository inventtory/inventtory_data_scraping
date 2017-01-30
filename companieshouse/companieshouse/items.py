# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CompanieshouseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    company_name = scrapy.Field()
    company_address = scrapy.Field()
    company_status = scrapy.Field()
    company_type = scrapy.Field()
    company_number = scrapy.Field()
    officer1_first_names = scrapy.Field()
    officer1_last_name = scrapy.Field()
    officer2_first_names = scrapy.Field()
    officer2_last_name = scrapy.Field()
    officer3_first_names = scrapy.Field()
    officer3_last_name = scrapy.Field()
    officer4_first_names = scrapy.Field()
    officer4_last_name = scrapy.Field()
    officer5_first_names = scrapy.Field()
    officer5_last_name = scrapy.Field()
    officer6_first_names = scrapy.Field()
    officer6_last_name = scrapy.Field()
    officer7_first_names = scrapy.Field()
    officer7_last_name = scrapy.Field()
    officer8_first_names = scrapy.Field()
    officer8_last_name = scrapy.Field()
    officer9_first_names = scrapy.Field()
    officer9_last_name = scrapy.Field()
    officer10_first_names = scrapy.Field()
    officer10_last_name = scrapy.Field()
    officer11_first_names = scrapy.Field()
    officer11_last_name = scrapy.Field()
    officer12_first_names = scrapy.Field()
    officer12_last_name = scrapy.Field()
    officer13_first_names = scrapy.Field()
    officer13_last_name = scrapy.Field()
    officer14_first_names = scrapy.Field()
    officer14_last_name = scrapy.Field()
    officer15_first_names = scrapy.Field()
    officer15_last_name = scrapy.Field()
    officer16_first_names = scrapy.Field()
    officer16_last_name = scrapy.Field()
    officer17_first_names = scrapy.Field()
    officer17_last_name = scrapy.Field()
    officer18_first_names = scrapy.Field()
    officer18_last_name = scrapy.Field()
    officer19_first_names = scrapy.Field()
    officer19_last_name = scrapy.Field()
    officer20_first_names = scrapy.Field()
    officer20_last_name = scrapy.Field()
    
    officer1_occupation = scrapy.Field()
    officer2_occupation = scrapy.Field()
    officer3_occupation = scrapy.Field()
    officer4_occupation = scrapy.Field()
    officer5_occupation = scrapy.Field()
    officer6_occupation = scrapy.Field()
    officer7_occupation = scrapy.Field()
    officer8_occupation = scrapy.Field()
    officer9_occupation = scrapy.Field()
    officer10_occupation = scrapy.Field()
    officer11_occupation = scrapy.Field()
    officer12_occupation = scrapy.Field()
    officer13_occupation = scrapy.Field()
    officer14_occupation = scrapy.Field()
    officer15_occupation = scrapy.Field()
    officer16_occupation = scrapy.Field()
    officer17_occupation = scrapy.Field()
    officer18_occupation = scrapy.Field()
    officer19_occupation = scrapy.Field()
    officer20_occupation = scrapy.Field()

    officer1_status = scrapy.Field()
    officer2_status = scrapy.Field()
    officer3_status = scrapy.Field()
    officer4_status = scrapy.Field()
    officer5_status = scrapy.Field()
    officer6_status = scrapy.Field()
    officer7_status = scrapy.Field()
    officer8_status = scrapy.Field()
    officer9_status = scrapy.Field()
    officer10_status = scrapy.Field()
    officer11_status = scrapy.Field()
    officer12_status = scrapy.Field()
    officer13_status = scrapy.Field()
    officer14_status = scrapy.Field()
    officer15_status = scrapy.Field()
    officer16_status = scrapy.Field()
    officer17_status = scrapy.Field()
    officer18_status = scrapy.Field()
    officer19_status = scrapy.Field()
    officer20_status = scrapy.Field()
    
    #(SIC)
    nature_of_business = scrapy.Field()

    # for testing
    officers_url = scrapy.Field()

    #meta data
    query_number = scrapy.Field()
    record_number = scrapy.Field()
    email_address = scrapy.Field()
    test = scrapy.Field()

    #6 get email addresses via automated Google search, based on:
    #Company Name and Officer LastName/FirstName
    officer1_email = scrapy.Field()
    officer2_email = scrapy.Field()
    officer3_email = scrapy.Field()
    officer4_email = scrapy.Field()
    officer5_email = scrapy.Field()
    
