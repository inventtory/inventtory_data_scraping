import sys
import csv
import os.path

csv.field_size_limit(sys.maxsize)

new_rows = []

###CHANGE DIRECTORY PATH AS REQUIRED###
save_path = 'C:\Users\serap\Documents\inventtory_data_scraping\inventtory_data_scraping\inventtory_spiders\DATA_OUTPUT1'
             

with open('uspto_classes_subclasse_test2.csv', "rt") as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        if i == 0:
            header = row
        else:
            new_rows.append(row)


#########################
###PROCESS DATA FIELDS###
#########################

fields = ['document_url', 'key_identifier', 'patent_country_code', 'patent_country', 'patent_application_number', 'patent_number', 'patent_name', 'patent_publish_date', 'patent_kind_code', 'abstract', 'inventors', 'applicant_1', 'applicant_2', 'applicant_3', 'applicant_4', 'applicant_5', 'applicant_6', 'applicant_7', 'applicant_8', 'applicant_9', 'applicant_10', 'assignee', 'family_ID', 'application_number', 'filed_date', 'pct_filed', 'pct_number', 'pct_pub_number', 'pct_pub_date', 'related_US_patent_document_1', 'related_US_patent_document_2', 'related_US_patent_document_3', 'related_US_patent_document_4', 'related_US_patent_document_5', 'related_US_patent_document_6', 'related_US_patent_document_7', 'related_US_patent_document_8', 'related_US_patent_document_9', 'related_US_patent_document_10', 'current_US_class', 'current_CPC_class', 'current_international_class', 'class_at_publication', 'international_class', 'field_of_search', 'prior_pub_data_document_identifier', 'prior_pub_data_publication_date', 'references_cited', 'references_primary_examiner', 'references_assistant_examiner', 'references_attorney_agent_or_firm', 'ref_cited_US_patent_documents', 'ref_cited_foreign_patent_documents', 'ref_cited_other_references', 'other_references', 'other_references_primary_examiner', 'other_references_assistant_examiner', 'other_references_attorney_agent_or_firm', 'patent_claims', 'parent_case_text', 'patent_description']

for record in new_rows:
    patent_index = header.index('key_identifier')
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


