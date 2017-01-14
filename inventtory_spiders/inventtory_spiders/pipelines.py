# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import os.path
import re
import textwrap
import csv
import time
import logging
from scrapy.utils.log import configure_logging
from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.exporters import CsvItemExporter
from inventtory_spiders import settings
from scrapy.settings import Settings

##################
###DATA OPTIONS###
##################

option_1 = 'Abstr-Claim-Descr'
option_2 = 'All-Fields'



class CountPipeline(object):

    def __init__(self, stats):
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)

    def process_item(self, item, spider):
        num = self.stats.get_value('item_scraped_count')
        if num == None:
            num = 1
            print("record number: " + str(num))
        else:
            num = num + 1
            print("record number: " + str(num))
        
        return item


class InventtorySpidersPipeline(object):

    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        print("We're in the pipeline!")
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        spider_name = str(spider.name)
        print(spider_name)
        ###OPTION 1###
        spider_path = '/Users/romerchris/Desktop/Desktop/Companies/inventtory/inventtory/PAMM/Complements/Scraping/Scrapy/inventtory_spiders_CHRIS_COPY/inventtory_data_scraping/inventtory_data_scraping/inventtory_spiders/' + spider_name + '_' + option_1
        ###OPTION 2###
        #spider_path = '/Users/romerchris/Desktop/Desktop/Companies/inventtory/inventtory/PAMM/Complements/Scraping/Scrapy/inventtory_spiders_CHRIS_COPY/inventtory_data_scraping/inventtory_data_scraping/inventtory_spiders/' + spider_name + '_' + option_2
        if not os.path.exists(spider_path):
            os.makedirs(spider_path)
            csv_path = spider_path + '/' + 'CSV_' + spider_name
            txt_path = spider_path + '/' + 'TXT_' + spider_name
            log_path = spider_path + '/' + 'LOG_' + spider_name
            if not os.path.exists(csv_path):
                os.makedirs(csv_path)
                os.makedirs(txt_path)
                os.makedirs(log_path)
                try:
                    len([name for name in os.listdir(csv_path) if os.path.isfile(os.path.join(csv_path, name))])
                    num = len([name for name in os.listdir(csv_path) if os.path.isfile(os.path.join(csv_path, name))]) + 1
                except:
                    num = 1
                name_of_csv = spider_name + '_' + str(num) + '.csv'
                new_file = open(csv_path +'/'+'%s_%d.csv' % (spider_name, num), 'w+b')
                self.files[spider] = new_file
                self.exporter = CsvItemExporter(new_file, 'data', 'row')

                ################
                ###SET SCHEMA###
                ################

                if 'espacenet' in spider_name:
                    self.exporter.fields_to_export = ['document_url', 'key_identifier', 'patent_country', 'patent_country_code', 'patent_application_number', 'patent_number', 'patent_name', 'page_bookmark', 'inventors', 'applicants', 'classification_international', 'classification_cooperative', 'application_number', 'priority_numbers', 'abstract', 'patent_description', 'original_claims', 'claims_tree', 'cited_documents', 'citing_documents', 'INPADOC_legal_status', 'INPADOC_patent_family']
                    self.exporter.start_exporting()
                elif 'uspto' in spider_name:
                    self.exporter.fields_to_export = ['document_url', 'key_identifier', 'patent_country_code', 'patent_country', 'patent_application_number', 'patent_number', 'patent_name', 'patent_publish_date', 'patent_kind_code', 'abstract', 'inventors', 'applicant_1', 'applicant_2', 'applicant_3', 'applicant_4', 'applicant_5', 'applicant_6', 'applicant_7', 'applicant_8', 'applicant_9', 'applicant_10', 'assignee', 'family_ID', 'application_number', 'filed_date', 'pct_filed', 'pct_number', 'pct_pub_number', 'pct_pub_date', 'related_US_patent_document_1', 'related_US_patent_document_2', 'related_US_patent_document_3', 'related_US_patent_document_4', 'related_US_patent_document_5', 'related_US_patent_document_6', 'related_US_patent_document_7', 'related_US_patent_document_8', 'related_US_patent_document_9', 'related_US_patent_document_10', 'current_US_class', 'current_CPC_class', 'current_international_class', 'class_at_publication', 'international_class', 'field_of_search', 'prior_pub_data_document_identifier', 'prior_pub_data_publication_date', 'references_cited', 'references_primary_examiner', 'references_assistant_examiner', 'references_attorney_agent_or_firm', 'ref_cited_US_patent_documents', 'ref_cited_foreign_patent_documents', 'ref_cited_other_references', 'other_references', 'other_references_primary_examiner', 'other_references_assistant_examiner', 'other_references_attorney_agent_or_firm', 'patent_claims', 'parent_case_text', 'patent_description']
                    self.exporter.start_exporting()
            else:
                try:
                    len([name for name in os.listdir(csv_path) if os.path.isfile(os.path.join(csv_path, name))])
                    num = len([name for name in os.listdir(csv_path) if os.path.isfile(os.path.join(csv_path, name))]) + 1
                except:
                    num = 1
                name_of_csv = spider_name + '_' + str(num) + '.csv'
                new_file=open(csv_path +'/'+'%s_%d.csv' % (spider_name, num), 'w+b')
                self.files[spider] = new_file
                self.exporter = CsvItemExporter(new_file, 'data', 'row')

                ################
                ###SET SCHEMA###
                ################

                if 'espacenet' in spider_name:
                    print('espacenet pipeline!')
                    self.exporter.fields_to_export = ['document_url', 'key_identifier', 'patent_country', 'patent_country_code', 'patent_application_number', 'patent_number', 'patent_name', 'page_bookmark', 'inventors', 'applicants', 'classification_international', 'classification_cooperative', 'application_number', 'priority_numbers', 'abstract', 'patent_description', 'original_claims', 'claims_tree', 'cited_documents', 'citing_documents', 'INPADOC_legal_status', 'INPADOC_patent_family']
                    self.exporter.start_exporting()
                elif 'uspto' in spider_name:
                    print('uspto pipeline!')
                    self.exporter.fields_to_export = ['document_url', 'key_identifier', 'patent_country_code', 'patent_country', 'patent_application_number', 'patent_number', 'patent_name', 'patent_publish_date', 'patent_kind_code', 'abstract', 'inventors', 'applicant_1', 'applicant_2', 'applicant_3', 'applicant_4', 'applicant_5', 'applicant_6', 'applicant_7', 'applicant_8', 'applicant_9', 'applicant_10', 'assignee', 'family_ID', 'application_number', 'filed_date', 'pct_filed', 'pct_number', 'pct_pub_number', 'pct_pub_date', 'related_US_patent_document_1', 'related_US_patent_document_2', 'related_US_patent_document_3', 'related_US_patent_document_4', 'related_US_patent_document_5', 'related_US_patent_document_6', 'related_US_patent_document_7', 'related_US_patent_document_8', 'related_US_patent_document_9', 'related_US_patent_document_10', 'current_US_class', 'current_CPC_class', 'current_international_class', 'class_at_publication', 'international_class', 'field_of_search', 'prior_pub_data_document_identifier', 'prior_pub_data_publication_date', 'references_cited', 'references_primary_examiner', 'references_assistant_examiner', 'references_attorney_agent_or_firm', 'ref_cited_US_patent_documents', 'ref_cited_foreign_patent_documents', 'ref_cited_other_references', 'other_references', 'other_references_primary_examiner', 'other_references_assistant_examiner', 'other_references_attorney_agent_or_firm', 'patent_claims', 'parent_case_text', 'patent_description']
                    self.exporter.start_exporting()

        else:
            csv_path = spider_path + '/' + 'CSV_' + spider_name
            txt_path = spider_path + '/' + 'TXT_' + spider_name
            log_path = spider_path + '/' + 'LOG_' + spider_name
            if not os.path.exists(csv_path):
                os.makedirs(csv_path)
                os.makedirs(txt_path)
                try:
                    len([name for name in os.listdir(csv_path) if os.path.isfile(os.path.join(csv_path, name))])
                    num = len([name for name in os.listdir(csv_path) if os.path.isfile(os.path.join(csv_path, name))]) + 1
                except:
                    num = 1
                name_of_csv = spider_name + '_' + str(num) + '.csv'
                new_file=open(csv_path + '/' + '%s_%d.csv' % (spider_name, num), 'w+b')
                self.files[spider] = new_file
                self.exporter = CsvItemExporter(new_file, 'data', 'row')
                
                ################
                ###SET SCHEMA###
                ################
                
                if 'espacenet' in spider_name:
                    print('espacenet pipeline!')
                    self.exporter.fields_to_export = ['document_url', 'key_identifier', 'patent_country', 'patent_country_code', 'patent_application_number', 'patent_number', 'patent_name', 'page_bookmark', 'inventors', 'applicants', 'classification_international', 'classification_cooperative', 'application_number', 'priority_numbers', 'abstract', 'patent_description', 'original_claims', 'claims_tree', 'cited_documents', 'citing_documents', 'INPADOC_legal_status', 'INPADOC_patent_family']
                    self.exporter.start_exporting()
                elif 'uspto' in spider_name:
                    print('uspto pipeline!')
                    self.exporter.fields_to_export = ['document_url', 'key_identifier', 'patent_country_code', 'patent_country', 'patent_application_number', 'patent_number', 'patent_name', 'patent_publish_date', 'patent_kind_code', 'abstract', 'inventors', 'applicant_1', 'applicant_2', 'applicant_3', 'applicant_4', 'applicant_5', 'applicant_6', 'applicant_7', 'applicant_8', 'applicant_9', 'applicant_10', 'assignee', 'family_ID', 'application_number', 'filed_date', 'pct_filed', 'pct_number', 'pct_pub_number', 'pct_pub_date', 'related_US_patent_document_1', 'related_US_patent_document_2', 'related_US_patent_document_3', 'related_US_patent_document_4', 'related_US_patent_document_5', 'related_US_patent_document_6', 'related_US_patent_document_7', 'related_US_patent_document_8', 'related_US_patent_document_9', 'related_US_patent_document_10', 'current_US_class', 'current_CPC_class', 'current_international_class', 'class_at_publication', 'international_class', 'field_of_search', 'prior_pub_data_document_identifier', 'prior_pub_data_publication_date', 'references_cited', 'references_primary_examiner', 'references_assistant_examiner', 'references_attorney_agent_or_firm', 'ref_cited_US_patent_documents', 'ref_cited_foreign_patent_documents', 'ref_cited_other_references', 'other_references', 'other_references_primary_examiner', 'other_references_assistant_examiner', 'other_references_attorney_agent_or_firm', 'patent_claims', 'parent_case_text', 'patent_description']
                    self.exporter.start_exporting()
                
            else:
                
                try:
                    len([name for name in os.listdir(csv_path) if os.path.isfile(os.path.join(csv_path, name))])
                    num = len([name for name in os.listdir(csv_path) if os.path.isfile(os.path.join(csv_path, name))]) + 1
                except:
                    num = 1
                name_of_csv = spider_name + '_' + str(num) + '.csv'
                new_file = open(csv_path + '/' + '%s_%d.csv' % (spider_name, num), 'w+b')
                self.files[spider] = new_file
                self.exporter = CsvItemExporter(new_file, 'data', 'row')

                ################
                ###SET SCHEMA###
                ################
                
                if 'espacenet' in spider_name:
                    print('espacenet pipeline!')
                    self.exporter.fields_to_export = ['document_url', 'key_identifier', 'patent_country', 'patent_country_code', 'patent_application_number', 'patent_number', 'patent_name', 'page_bookmark', 'inventors', 'applicants', 'classification_international', 'classification_cooperative', 'application_number', 'priority_numbers', 'abstract', 'patent_description', 'original_claims', 'claims_tree', 'cited_documents', 'citing_documents', 'INPADOC_legal_status', 'INPADOC_patent_family']
                    self.exporter.start_exporting()
                elif 'uspto' in spider_name:
                    print('uspto pipeline!')
                    self.exporter.fields_to_export = ['document_url', 'key_identifier', 'patent_country_code', 'patent_country', 'patent_application_number', 'patent_number', 'patent_name', 'patent_publish_date', 'patent_kind_code', 'abstract', 'inventors', 'applicant_1', 'applicant_2', 'applicant_3', 'applicant_4', 'applicant_5', 'applicant_6', 'applicant_7', 'applicant_8', 'applicant_9', 'applicant_10', 'assignee', 'family_ID', 'application_number', 'filed_date', 'pct_filed', 'pct_number', 'pct_pub_number', 'pct_pub_date', 'related_US_patent_document_1', 'related_US_patent_document_2', 'related_US_patent_document_3', 'related_US_patent_document_4', 'related_US_patent_document_5', 'related_US_patent_document_6', 'related_US_patent_document_7', 'related_US_patent_document_8', 'related_US_patent_document_9', 'related_US_patent_document_10', 'current_US_class', 'current_CPC_class', 'current_international_class', 'class_at_publication', 'international_class', 'field_of_search', 'prior_pub_data_document_identifier', 'prior_pub_data_publication_date', 'references_cited', 'references_primary_examiner', 'references_assistant_examiner', 'references_attorney_agent_or_firm', 'ref_cited_US_patent_documents', 'ref_cited_foreign_patent_documents', 'ref_cited_other_references', 'other_references', 'other_references_primary_examiner', 'other_references_assistant_examiner', 'other_references_attorney_agent_or_firm', 'patent_claims', 'parent_case_text', 'patent_description']
                    self.exporter.start_exporting()

        ################################
        ###GENERATE CONVERSION SCRIPT###
        ################################
                
        new_rows = []

        if 'espacenet' in spider_name:
            convert_script = 'format_data_ESPACENET.py'
        elif 'uspto' in spider_name:
            convert_script = 'format_data_USPTO.py'

        if not os.path.exists(spider_path):
            os.makedirs(spider_path)
            with open(convert_script) as f_old:
                reader = f_old.readlines()
                for i, row in enumerate(reader):
                    new_rows.append(row)
            find1 = re.match('(.*?=\s*)?\'\/Users.*',new_rows[12]).group(1)
            find2 = re.match('with\s*open\(\'(.*?)\'.*',new_rows[15]).group(1)
            #FILE PATH - new_rows[12]
            new_rows[12] = find1 + '\'' + txt_path + '\''
            #FILE NAME - new_rows[15]   
            new_rows[15] = new_rows[15].replace(find2, 'CSV_' + spider_name + '/' + name_of_csv)
            name_of_file = "convert_" + spider_name + ".py"
            complete_name = os.path.join(spider_path, name_of_file)
            f_new = open(complete_name,"w")
            for i, line in enumerate(new_rows):
                print(line)
                f_new.write(line)
            f_new.close()
        else:
            with open(convert_script) as f_old:
                reader = f_old.readlines()
                for i, row in enumerate(reader):
                    new_rows.append(row)
            find1 = re.match('(.*?=\s*)?\'\/Users.*',new_rows[12]).group(1)
            find2 = re.match('with\s*open\(\'(.*?)\'.*',new_rows[15]).group(1)
            #FILE PATH - new_rows[12]
            new_rows[12] = find1 + '\'' + txt_path + '\''
            #FILE NAME - new_rows[15]   
            new_rows[15] = new_rows[15].replace(find2, 'CSV_' + spider_name + '/' + name_of_csv)
            name_of_file = "convert_" + spider_name + ".py"
            complete_name = os.path.join(spider_path, name_of_file)
            f_new = open(complete_name,"w")
            for i, line in enumerate(new_rows):
                print(line)
                f_new.write(line)
            f_new.close()
        
            

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        new_file = self.files.pop(spider)
        new_file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item






    
