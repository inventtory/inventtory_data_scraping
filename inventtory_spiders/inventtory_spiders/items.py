# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class EspacenetItem(scrapy.Item):

    ###doucument_url###
    document_url = scrapy.Field()
    
    ###TAB1 - Bibliographic data##
    key_identifier = scrapy.Field()
    patent_kind_code = scrapy.Field()
    patent_country = scrapy.Field() 
    patent_country_code = scrapy.Field()
    patent_application_number = scrapy.Field()
    patent_number = scrapy.Field()
    patent_name = scrapy.Field()
    page_bookmark = scrapy.Field()
    inventors = scrapy.Field()
    applicants = scrapy.Field()
    classification_international = scrapy.Field()
    classification_cooperative = scrapy.Field()
    application_number = scrapy.Field()
    priority_numbers = scrapy.Field()
    abstract = scrapy.Field()

    ###TAB2 - Description###

    patent_description = scrapy.Field()

    ###TAB3 - Claims###

    original_claims = scrapy.Field()
    claims_tree = scrapy.Field()
    
    ###TAB4 - Cited documents###

    cited_documents = scrapy.Field()
  
    ###TAB5 - Citing documents###

    citing_documents =  scrapy.Field()
    
    ###TAB6 - INPADOC legal status###

    INPADOC_legal_status = scrapy.Field()
    
    ###TAB7 - INPADOC patent family###

    INPADOC_patent_family = scrapy.Field()


class UsptoItem(scrapy.Item):

    document_url = scrapy.Field()
    key_identifier = scrapy.Field()
    patent_country_code = scrapy.Field()
    patent_country = scrapy.Field() 
    patent_application_number = scrapy.Field()
    patent_number = scrapy.Field()
    patent_name = scrapy.Field()
    patent_publish_date = scrapy.Field()
    patent_kind_code = scrapy.Field()
    abstract = scrapy.Field()
    inventors = scrapy.Field()
    applicant_1 = scrapy.Field()
    applicant_2 = scrapy.Field()
    applicant_3 = scrapy.Field()
    applicant_4 = scrapy.Field()
    applicant_5 = scrapy.Field()
    applicant_6 = scrapy.Field()
    applicant_7 = scrapy.Field()
    applicant_8 = scrapy.Field()
    applicant_9 = scrapy.Field()
    applicant_10 = scrapy.Field()
    assignee = scrapy.Field()
    family_ID = scrapy.Field()
    application_number = scrapy.Field()
    filed_date = scrapy.Field()
    pct_filed = scrapy.Field()
    pct_number = scrapy.Field()
    pct_pub_number = scrapy.Field()
    pct_pub_date = scrapy.Field()
    related_US_patent_document_1 = scrapy.Field()
    related_US_patent_document_2 = scrapy.Field()
    related_US_patent_document_3 = scrapy.Field()
    related_US_patent_document_4 = scrapy.Field()
    related_US_patent_document_5 = scrapy.Field()
    related_US_patent_document_6 = scrapy.Field()
    related_US_patent_document_7 = scrapy.Field()
    related_US_patent_document_8 = scrapy.Field()
    related_US_patent_document_9 = scrapy.Field()
    related_US_patent_document_10 = scrapy.Field()
    current_US_class = scrapy.Field()
    current_CPC_class = scrapy.Field()
    current_international_class = scrapy.Field()
    class_at_publication = scrapy.Field()
    international_class = scrapy.Field()
    field_of_search = scrapy.Field()
    prior_pub_data_document_identifier = scrapy.Field()
    prior_pub_data_publication_date = scrapy.Field()
    references_cited = scrapy.Field()
    references_primary_examiner = scrapy.Field()
    references_assistant_examiner = scrapy.Field()
    references_attorney_agent_or_firm = scrapy.Field()
    ref_cited_US_patent_documents = scrapy.Field()
    ref_cited_foreign_patent_documents = scrapy.Field()
    ref_cited_other_references = scrapy.Field()
    other_references = scrapy.Field()
    other_references_primary_examiner = scrapy.Field()
    other_references_assistant_examiner = scrapy.Field()
    other_references_attorney_agent_or_firm = scrapy.Field()
    patent_claims = scrapy.Field()
    parent_case_text = scrapy.Field()
    patent_description = scrapy.Field()


class TestItem(scrapy.Item):
    page_number = scrapy.Field()
    patent_link_number = scrapy.Field()
    patent_name = scrapy.Field()
    patent_url = scrapy.Field()
    tab_1 = scrapy.Field()
    tab_2 = scrapy.Field()
    tab_3 = scrapy.Field()
    tab_4 = scrapy.Field()
    tab_5 = scrapy.Field()
    tab_6 = scrapy.Field()
    tab_7 = scrapy.Field()











    
    

