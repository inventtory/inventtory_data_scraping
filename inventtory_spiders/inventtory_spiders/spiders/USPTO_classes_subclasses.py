# -*- coding: utf-8 -*-

import scrapy
import re
import json
import csv
import urllib
from bs4 import BeautifulSoup
from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from inventtory_spiders.items import UsptoItem



class UsptoSpider(CrawlSpider):
    name = "uspto_classes_subclasses"
    #generate search urls
    def start_requests(self):
        classes_subclasses = ['177/136','180/273','701/517','296/$']
        codes = ''
        for code in classes_subclasses:
            codes = codes + 'CCL/' + str(code) + ' OR '
        codes = codes[:-4]  
        url = 'http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=0&p=1&f=S&l=50&Query=' + str(codes) + '&d=PTXT'    
        #test
        print(url)
        yield Request(url, callback=self.parse_search_url, dont_filter=True)


    def parse_search_url(self, response):
        ## get URL ##
        get = response
        url = re.match('<200\s*(.*?)>', str(get)).group(1)
        url1 = re.match('(.*?&p=)\d+(.*)',url).group(1)
        url2 = re.match('(.*?&p=)\d+(.*)',url).group(2)


        
        ## Work out number of pages from number of patents for each query result
        num_patents = response.xpath('//i[contains(text(),"Hits")]//text()').extract()
        find = num_patents.index(' out of ') + 1
        num_patents = int(num_patents[find].strip())
        print("total number of records is: " + str(num_patents))
        
        if num_patents % 50 != 0:
            num_pages = int(num_patents/50)+1
        else:
            num_pages = int(num_patents/50)

        print("total numbers of pages is: " + str(num_pages))

        #generate url
        for n in range(1,num_pages+1):
            page = url1 + str(n) + url2
            yield Request(page, callback=self.parse_next_page, dont_filter=True)

    ## Drill into patent links
    def parse_next_page(self, response):
        get = response
        url = re.match('<200\s*(.*?)>', str(get)).group(1)
        #get patent link
        links = response.xpath('//tr//td[2][@valign="top"]/a/@href').extract()
        links = ['http://patft.uspto.gov' + e for e in links]
        for patent_link in links:
            yield Request(patent_link, callback=self.parse_patent)


    def parse_patent(self, response):
        
        #test we got here
        print("we're here!")
        
        #get current url
        get = response
        url = re.match('<200\s*(.*?)>', str(get)).group(1)
        item = UsptoItem()
            

        ############
        ###SCHEMA###
        ############
        #0 document_url
        item['document_url'] = url

        #1 patent_number
        if response.xpath('//title/text()').re('United\s*States\s*Patent:\s*([0-9a-zA-Z]{1}[0-9]{6})') != []:
            patent_number = response.xpath('//title/text()').re('United\s*States\s*Patent:\s*([0-9a-zA-Z]{1}[0-9]{6})')[0]
            item['patent_number'] = 'US' + str(patent_number) + 'B2'
        else:
            item['patent_number'] = ''

        #1b country_code
        patent_country_code = 'US'
        item['patent_country_code'] = 'US'
        #1c patent_country
        patent_country = 'United States'
        item['patent_country'] = 'United States'

        #2 patent_name
        if response.xpath('//font[@size="+1"]/text()') != []:
            patent_name = response.xpath('//font[@size="+1"]/text()').extract()[0]
            item['patent_name'] = patent_name = patent_name.replace('\n','')
        else:
            item['patent_name'] = ''

        #3 patent_publish_date
        item['patent_publish_date'] = response.xpath('//body//tr//td[2]/b/text()').re('.*?(\w+\s*\d+\s*,?\s*(?:19|20)\d{2}).*')[0]

        #4 patent_type
        patent_kind_code = 'B2'
        item['patent_kind_code'] = 'B2'

        #4b key_identifier
        key_identifier = str(patent_country_code) + str(patent_number) + str(patent_kind_code)
        item['key_identifier'] = key_identifier

        #5 abstract
        if response.xpath('//b[contains(text(),"Abstract")]').xpath('//p/text()') != []:
            abstract = response.xpath('//b[contains(text(),"Abstract")]').xpath('//p/text()').extract()
            item['abstract'] = ''.join(abstract)
        else:
            item['abstract'] = ''
                
        #6 inventors
        if response.xpath('//table//tr[1]/td[1]//text()') != []:
            inventors = response.xpath('//table//tr[1]/td[1]//text()').extract()
            clean = [e for e in inventors if '\n' not in e]
            beg = clean.index('United States Patent ')+1
            end = clean.index('Current U.S. Class:')
            clean = clean[beg:end]
            item['inventors'] = ''.join(clean)
        else:
            item['inventors'] = ''
            
        #7 applicants - contains all applicant-related data
        applicants = []
        if response.xpath('//tr').re('Applicant(?:.*\n)+.*') != []:
            applicants = response.xpath('//tr').re('Applicant(?:.*\n)+.*')
            clean = applicants[0].split('<td>')
            names = clean[1]
            names = names.split('<i>')[1:]
            names = [BeautifulSoup(e,"lxml").findAll(text=True) for e in names]
            names = [e[0].strip() for e in names if (e != ' ') or (e != '')]
            locations = clean[2]
            locations = BeautifulSoup(locations,"lxml")
            locations = locations.findAll(text=True) #debug
            locations = [str(e).strip() for e in locations if (e != ' ') and (e != '')]
            no_apps = len(locations)
            city_index = (int(no_apps/3)*1)
            cities = locations[:city_index]
            state_index = (int(no_apps/3)*2)
            states = locations[city_index:state_index]
            country_index = (int(no_apps/3)*3)
            countries = locations[state_index:country_index]

            for i, entry in enumerate(names):
                applicant = ''
                applicant = 'Name: ' + str(entry) + ', ' + 'City: ' + str(cities[i]) + ', ' + 'State: ' + str(states[i]) + ', ' + 'Country: ' + str(countries[i])
                i += 1
                item['applicant_'+str(i)] = applicant
                
        #9 assignee
        if response.xpath('//tr').re('.*?Assignee.*(?:\n+.*)+?<\/tr>.*') != []:
            assignee = response.xpath('//tr').re('.*?Assignee.*(?:\n+.*)+?<\/tr>.*')[0]
            html = str(assignee)
            soup = BeautifulSoup(html,"lxml")
            data = soup.findAll(text=True)
            data = ''.join(data)
            data = data.replace(re.match('.*?(\n)+.*',data).group(1), ' ')
            item['assignee'] = data
        else:
            item['assignee'] = ''
                
            
        #10 family_ID
        if response.xpath('//tr').re('Family\s*ID.*(?:\n+.*)+?<b>([0-9]{8,}).*') != []:
            item['family_ID'] = int(response.xpath('//tr').re('Family\s*ID.*(?:\n+.*)+?<b>([0-9]{8,}).*')[0])
        else:
            item['family_ID'] = []
            

        #11 application_number
        if response.xpath('//tr').re('Appl\.\s*No\.:.*(?:\n+.*)+?<b>(\d+\/\d+,?\d+).*') != []:
            item['application_number'] = response.xpath('//tr').re('Appl\.\s*No\.:.*(?:\n+.*)+?<b>(\d+\/\d+,?\d+).*')[0]
        else:
            item['application_number'] = ''
                

        #12 filed_date
        if response.xpath('//tr').re('Filed:.*(?:\n+.*)+?<b>(\w+\s*\d+,?\s*(?:18|19|20)\d{2}).*') != []:
            item['filed_date'] = response.xpath('//tr').re('Filed:.*(?:\n+.*)+?<b>(\w+\s*\d+,?\s*(?:18|19|20)\d{2}).*')[0]
        else:
            item['filed_date'] = ''

        ###TO BE POULATED AS AND WHEN FIND EXAMPLE###
        #13 pct_filed
        #pct_filed = scrapy.Field()

        #14 pct_number
        #pct_number = scrapy.Field()
        
        #371(c)(1),(2),(4) Date: what is this?

        #15 pct_pub_number
        #pct_pub_number = scrapy.Field()

        #16 pct_pub_date
        #pct_pub_date = scrapy.Field()
        

        #17 current_US_class
        if response.xpath('//tr/td/b[contains(text(), "Current U.S. Class:")]').xpath('//td[2]/b/text()').re('\d+\/\d+') != []:
            item['current_US_class'] = response.xpath('//tr/td/b[contains(text(), "Current U.S. Class:")]').xpath('//td[2]/b/text()').re('\d+\/\d+')[0]
        else:
            item['current_US_class'] = ''

        #17b current_cpc_class - test for this
        if response.xpath('//tr/td/b[contains(text(), "Current CPC Class:")]').xpath('//td[2]/text()') != []:
            current_CPC_class = response.xpath('//tr/td/b[contains(text(), "Current CPC Class:")]').xpath('//td[2]//text()').extract()
            beg = [current_CPC_class.index(str(e)) for e in current_CPC_class if re.match('([0-9a-zA-Z]+\s*\d+\/.*?\(\d+\);?).*', e)]
            try:
                beg[0]
                b1 = beg[0]
                item['current_CPC_class'] = current_CPC_class[b1]
            except:
                item['current_CPC_class'] = ''


            #18 current_international_class - test for this
            try:
                beg[1]
                b2 = beg[1]
                item['current_international_class'] = current_CPC_class[b2]
            except:
                item['current_international_class'] = ''
        else:
            item['current_CPC_class'] = ''
            item['current_international_class'] = ''
                

            

        #19 field_of_search
        if response.xpath('//tr/td/b[contains(text(), "Field of Search:")]').xpath('//td[2]/text()') != []:
            field_of_search = response.xpath('//tr/td/b[contains(text(), "Field of Search:")]').xpath('//td[2]/text()').re('(;[0-9a-zA-Z.,]+\/?[0-9a-zA-Z.,]+)+')
            item['field_of_search'] = ' '.join(field_of_search)
        else:
            item['field_of_search'] = ''
            
        
        #20 prior_pub_data_document_identifier
        if response.xpath('//center/b[contains(text(), "Prior Publication Data")]').xpath('//tr/td/text()').re('\w{2}\s*(?:18|19|20)\d{2}[0-9a-zA-Z]{7}\s*\w{2}') != []:
            item['prior_pub_data_document_identifier'] = response.xpath('//center/b[contains(text(), "Prior Publication Data")]').xpath('//tr/td/text()').re('\w{2}\s*(?:18|19|20)\d{2}[0-9a-zA-Z]{7}\s*\w{2}')[0]
        else:
            item['prior_pub_data_document_identifier'] = ''


        #21 prior_pub_data_publication_date
        if response.xpath('//center/b[contains(text(), "Prior Publication Data")]').xpath('//tr/td/text()').re('\w+\s*\d+,?\s*(?:18|19|20)\d{2}') != []:
            item['prior_pub_data_publication_date'] = response.xpath('//center/b[contains(text(), "Prior Publication Data")]').xpath('//tr/td/text()').re('\w+\s\d+,?\s(?:18|19|20)\d{2}')[0]
        else:
            item['prior_pub_data_publication_date'] = ''
            
            
        #22 related_US_patent_app_number
        if response.xpath('//center/b[contains(text(), "Related U.S. Patent Documents")]').xpath('//tr//text()') != []:
            get_data = response.xpath('//center/b[contains(text(), "Related U.S. Patent Documents")]').xpath('//tr//text()').extract()
            beg = [get_data.index('Application Number') for e in get_data if 'Application Number' in e][0]
            end = [get_data.index('Current U.S. Class:') for e in get_data if 'Current U.S. Class:' in e][0]
            get_values = get_data[beg:end]
            data = get_values[3:]
            data = [e for e in data if '\n' not in e]
            no_records = int(len(data)/3)
            marker = 0
            #documents = []
            for num in range(1,no_records+1):
                entry = []
                entry = data[marker:int(len(data)/no_records)*num]
                entry = ', '.join(entry)
                marker = int(len(data)/no_records)*num
                item['related_US_patent_document_'+str(num)] = entry
                
        else:
            item['related_US_patent_document_1'] = ''
                

        #26 references_cited
        if response.xpath('//tr').re('<a\s*href.*?\d{7}(?:.*\n+)+.*?\w+\s*(?:18|19|20)\d{2}<\/td>(?:.*\n+)+.*?\w+.*') != []:
            references_cited = []
            get_references = response.xpath('//tr').re('<a\s*href.*?\d{7}(?:.*\n+)+.*?\w+\s*(?:18|19|20)\d{2}<\/td>(?:.*\n+)+.*?\w+.*')
            for reference in get_references:
                html = str(reference)
                soup = BeautifulSoup(html,"lxml")
                text_data = soup.findAll(text=True)
                link = soup.findAll('a',href=True)
                link = 'http://patft.uspto.gov' + re.match('<a\s*href=\"(.*?)?\".*',str(link[0])).group(1)
                clean_data = [e.replace('\n',', ') for e in text_data]
                clean_data = ''.join(clean_data)
                everything = link + ', ' + clean_data
                references_cited.append(everything)

            item['references_cited'] = references_cited
        else:
            item['references_cited'] = ''
                
            

        #32 other_references
        #other_references = scrapy.Field()

        #33 references_primary_examiner
        if response.xpath('//i').xpath('//text()') != []:
            find_text = response.xpath('//i').xpath('//text()').extract()
            beg = [find_text.index('Primary Examiner:') for e in find_text if 'Primary Examiner:' in e][0]
            if 'Parent Case Text' in find_text:
                end = [find_text.index('Parent Case Text') for e in find_text if 'Parent Case Text' in e][0]
            else:
                end = [find_text.index('Description') for e in find_text if 'Description' in e][0]
                
            ref_info = find_text[beg:end]
            clean = [e.strip()  for e in ref_info]
            clean = [e for e in clean if e != '']
            #find rel data
            if ('Primary Examiner:' in clean) == True:
                find_1 = clean.index('Primary Examiner:')+1
                item['references_primary_examiner'] = clean[find_1]
            else:
                item['references_primary_examiner'] = ''
                    
            if ('Assistant Examiner:' in clean) == True:
                find_2 = clean.index('Assistant Examiner:')+1
                #34 references_assistant_examiner
                item['other_references_assistant_examiner'] = clean[find_2]
            else:
                item['other_references_assistant_examiner'] = ''

            if ('Attorney, Agent or Firm:' in clean) == True:
                find_3 = clean.index('Attorney, Agent or Firm:')+1
                #35 references_attorney_agent_or_firm
                item['other_references_attorney_agent_or_firm'] = clean[find_3]
            else:
                item['other_references_attorney_agent_or_firm'] = ''
     
        else:
            item['references_primary_examiner'] = ''
            item['other_references_assistant_examiner'] = ''
            item['other_references_attorney_agent_or_firm'] = ''

                

        #get claims and description
        if response.xpath('//html//body//coma//text()') != []:
            text_data = response.xpath('//html//body//coma//text()').extract()
            if 'Claims' in text_data:
                text_data = ''.join(text_data)
                claims_index = text_data.index('Claims')
                desc_index = text_data.index('Description')
                #get description
                description = text_data[desc_index:]
                description = description.replace(re.match('.*?(Description\s*).*',description).group(1),'')
                item['patent_description'] = description
                #get claims
                claims = text_data[claims_index:desc_index]
                claims = claims.replace(re.match('.*?(Claims\s*).*',claims).group(1),'')
                item['patent_claims'] = claims
            else:
                text_data = ''.join(text_data)
                desc_index = text_data.index('Description')
                
                #get description
                description = text_data[desc_index:]
                description = description.replace(re.match('.*?(Description\s*).*',description).group(1),'')
                item['patent_description'] = description
                #get claims
                claims = response.xpath('//body//text()').re('.*CLAIM(?:.*\n*.*)+')[0]
                item['patent_claims'] = claims.replace(re.match('((?:.*\n+.*)*.*CLAIM\n*\s*).*', claims).group(1), '').strip()
                
                
        else:
            item['patent_claims'] = ''
            item['patent_description'] = ''
                
            
            
        yield item

      
                    
                    
#scrapy crawl uspto_classes_subclasses -o uspto_classes_subclasse_test2.csv
