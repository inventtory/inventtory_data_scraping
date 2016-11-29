# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import scrapy
import re
import json
import csv
import requests
from bs4 import BeautifulSoup
from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from inventtory_spiders.items import EspacenetItem



class EspacenetSpider(CrawlSpider):
    name = "espacenet_europe"
    def start_requests(self):
        #search european patents
        url = "https://worldwide.espacenet.com/data/searchResults?submitted=true&locale=en_EP&DB=EPODOC&ST=advanced&TI=&AB=&PN=EP&AP=&PR=&PD=&PA=&IN=&CPC=&IC=&Submit=Search"
        yield Request(url, callback=self.parse_query_url, dont_filter=True)



    def parse_query_url(self, response):
        get = response
        url = re.match('<200\s*(.*?)>', str(get)).group(1)
        url1 = re.match('(https:\/\/worldwide\.espacenet\.com\/data\/searchResults\?)submitted=true(.*)',url).group(1)
        url2 = re.match('(https:\/\/worldwide\.espacenet\.com\/data\/searchResults\?)submitted=true(.*)',url).group(2)

        #extract number of items
        if response.xpath('//div[@class="epoBarItem "]//text()') != []:
            num_results = response.xpath('//div[@class="epoBarItem "]//text()').extract()
        else:
            num_results = response.xpath('//div[@class="epoBarItem wordBreakDiv"]//text()').extract()
        clean = ''.join(num_results).strip()
        if "Approximately" in clean:
            clean = re.match('.*?Approximately\s*(\d+,?\d+)\s*results\s*found.*', clean).group(1)
            num_results = int(clean.replace(',',''))
        elif re.match('(\d+)\s*results\s*found.*',clean) is not None:
            clean = re.match('(\d+)\s*results\s*found.*',clean).group(1)
            num_results = int(clean.replace(',',''))
        else:
            clean = re.match('More\s*than\s*(\d+,?\d+)\s*results.*',clean).group(1)
            num_results = int(clean.replace(',',''))



        #number of pages
        if (num_results % 25) == 0:
            num_pages = int(num_results/25)
        else:
            num_pages = int(num_results/25) + 1

        #test
        print(num_pages)

        #iterate through pages
        i = 0
        for num in range(0,num_pages):
            page = url1 + 'page=' + str(i) + url2
            i += 1
            yield Request(page, callback=self.parse_results, dont_filter=True)


    def parse_results(self, response):
        patent_links = response.xpath('//a[@class="publicationLinkClass"]/@href').extract()
        patent_links = ['https://worldwide.espacenet.com/data' + str(e) for e in patent_links]
        for patent_link in patent_links:
            yield Request(patent_link, callback=self.parse_patent_link, dont_filter=True)

    
            

    def parse_patent_link(self, response):
        #get current url, and process URL for next tab
        get = response
        url = re.match('<200\s*(.*?)>', str(get)).group(1)
        url1 = re.match('(https:\/\/worldwide\.espacenet\.com\/data\/publicationDetails\/)\w+(\?.*)',url).group(1)
        url2 = re.match('(https:\/\/worldwide\.espacenet\.com\/data\/publicationDetails\/)\w+(\?.*)',url).group(2)

        #test we've got here...
        print("We are here!")

        ##############################
        ###TAB1: Bibliographic data###
        ##############################

        item = EspacenetItem()

        item['document_url'] = url

        patent_country_code = response.xpath('//div[@id="pagebody"]//h1//text()').re('.*?(\w{2})\w{0,1}\d{6}.*')[0]
        item['patent_country_code'] = response.xpath('//div[@id="pagebody"]//h1//text()').re('.*?(\w{2})\w{0,1}\d{6}.*')[0]        #map country code to country name

        #list of mappings
        country_mappings = [['Afghanistan', 'AF'], ['Albania', 'AL'], ['Algeria', 'DZ'], ['American Samoa', 'AS'], ['Andorra', 'AD'], ['Angola', 'AO'], ['Anguilla', 'AI'], ['Antarctica', 'AQ'], ['Antigua and Barbuda', 'AG'], ['Argentina', 'AR'], ['Armenia', 'AM'], ['Aruba', 'AW'], ['Australia', 'AU'], ['Austria', 'AT'], ['Azerbaijan', 'AZ'], ['Bahamas', 'BS'], ['Bahrain', 'BH'], ['Bangladesh', 'BD'], ['Barbados', 'BB'], ['Belarus', 'BY'], ['Belgium', 'BE'], ['Belize', 'BZ'], ['Benin', 'BJ'], ['Bermuda', 'BM'], ['Bhutan', 'BT'], ['Bolivia', 'BO'], ['Bosnia and Herzegovina', 'BA'], ['Botswana', 'BW'], ['Brazil', 'BR'], ['British Indian Ocean Territory', 'IO'], ['British Virgin Islands', 'VG'], ['Brunei', 'BN'], ['Bulgaria', 'BG'], ['Burkina Faso', 'BF'], ['Burundi', 'BI'], ['Cambodia', 'KH'], ['Cameroon', 'CM'], ['Canada', 'CA'], ['Cape Verde', 'CV'], ['Cayman Islands', 'KY'], ['Central African Republic', 'CF'], ['Chad', 'TD'], ['Chile', 'CL'], ['China', 'CN'], ['Christmas Island', 'CX'], ['Cocos Islands', 'CC'], ['Colombia', 'CO'], ['Comoros', 'KM'], ['Cook Islands', 'CK'], ['Costa Rica', 'CR'], ['Croatia', 'HR'], ['Cuba', 'CU'], ['Curacao', 'CW'], ['Cyprus', 'CY'], ['Czech Republic', 'CZ'], ['Democratic Republic of the Congo', 'CD'], ['Denmark', 'DK'], ['Djibouti', 'DJ'], ['Dominica', 'DM'], ['Dominican Republic', 'DO'], ['East Timor', 'TL'], ['Ecuador', 'EC'], ['Egypt', 'EG'], ['El Salvador', 'SV'], ['Equatorial Guinea', 'GQ'], ['Eritrea', 'ER'], ['Estonia', 'EE'], ['Ethiopia', 'ET'], ['Falkland Islands', 'FK'], ['Faroe Islands', 'FO'], ['Fiji', 'FJ'], ['Finland', 'FI'], ['France', 'FR'], ['French Polynesia', 'PF'], ['Gabon', 'GA'], ['Gambia', 'GM'], ['Georgia', 'GE'], ['Germany', 'DE'], ['Ghana', 'GH'], ['Gibraltar', 'GI'], ['Greece', 'GR'], ['Greenland', 'GL'], ['Grenada', 'GD'], ['Guam', 'GU'], ['Guatemala', 'GT'], ['Guernsey', 'GG'], ['Guinea', 'GN'], ['Guinea-Bissau', 'GW'], ['Guyana', 'GY'], ['Haiti', 'HT'], ['Honduras', 'HN'], ['Hong Kong', 'HK'], ['Hungary', 'HU'], ['Iceland', 'IS'], ['India', 'IN'], ['Indonesia', 'ID'], ['Iran', 'IR'], ['Iraq', 'IQ'], ['Ireland', 'IE'], ['Isle of Man', 'IM'], ['Israel', 'IL'], ['Italy', 'IT'], ['Ivory Coast', 'CI'], ['Jamaica', 'JM'], ['Japan', 'JP'], ['Jersey', 'JE'], ['Jordan', 'JO'], ['Kazakhstan', 'KZ'], ['Kenya', 'KE'], ['Kiribati', 'KI'], ['Kosovo', 'XK'], ['Kuwait', 'KW'], ['Kyrgyzstan', 'KG'], ['Laos', 'LA'], ['Latvia', 'LV'], ['Lebanon', 'LB'], ['Lesotho', 'LS'], ['Liberia', 'LR'], ['Libya', 'LY'], ['Liechtenstein', 'LI'], ['Lithuania', 'LT'], ['Luxembourg', 'LU'], ['Macau', 'MO'], ['Macedonia', 'MK'], ['Madagascar', 'MG'], ['Malawi', 'MW'], ['Malaysia', 'MY'], ['Maldives', 'MV'], ['Mali', 'ML'], ['Malta', 'MT'], ['Marshall Islands', 'MH'], ['Mauritania', 'MR'], ['Mauritius', 'MU'], ['Mayotte', 'YT'], ['Mexico', 'MX'], ['Micronesia', 'FM'], ['Moldova', 'MD'], ['Monaco', 'MC'], ['Mongolia', 'MN'], ['Montenegro', 'ME'], ['Montserrat', 'MS'], ['Morocco', 'MA'], ['Mozambique', 'MZ'], ['Myanmar', 'MM'], ['Namibia', 'NA'], ['Nauru', 'NR'], ['Nepal', 'NP'], ['Netherlands', 'NL'], ['Netherlands Antilles', 'AN'], ['New Caledonia', 'NC'], ['New Zealand', 'NZ'], ['Nicaragua', 'NI'], ['Niger', 'NE'], ['Nigeria', 'NG'], ['Niue', 'NU'], ['North Korea', 'KP'], ['Northern Mariana Islands', 'MP'], ['Norway', 'NO'], ['Oman', 'OM'], ['Pakistan', 'PK'], ['Palau', 'PW'], ['Palestine', 'PS'], ['Panama', 'PA'], ['Papua New Guinea', 'PG'], ['Paraguay', 'PY'], ['Peru', 'PE'], ['Philippines', 'PH'], ['Pitcairn', 'PN'], ['Poland', 'PL'], ['Portugal', 'PT'], ['Puerto Rico', 'PR'], ['Qatar', 'QA'], ['Republic of the Congo', 'CG'], ['Reunion', 'RE'], ['Romania', 'RO'], ['Russia', 'RU'], ['Rwanda', 'RW'], ['Saint Barthelemy', 'BL'], ['Saint Helena', 'SH'], ['Saint Kitts and Nevis', 'KN'], ['Saint Lucia', 'LC'], ['Saint Martin', 'MF'], ['Saint Pierre and Miquelon', 'PM'], ['Saint Vincent and the Grenadines', 'VC'], ['Samoa', 'WS'], ['San Marino', 'SM'], ['Sao Tome and Principe', 'ST'], ['Saudi Arabia', 'SA'], ['Senegal', 'SN'], ['Serbia', 'RS'], ['Seychelles', 'SC'], ['Sierra Leone', 'SL'], ['Singapore', 'SG'], ['Sint Maarten', 'SX'], ['Slovakia', 'SK'], ['Slovenia', 'SI'], ['Solomon Islands', 'SB'], ['Somalia', 'SO'], ['South Africa', 'ZA'], ['South Korea', 'KR'], ['South Sudan', 'SS'], ['Spain', 'ES'], ['Sri Lanka', 'LK'], ['Sudan', 'SD'], ['Suriname', 'SR'], ['Svalbard and Jan Mayen', 'SJ'], ['Swaziland', 'SZ'], ['Sweden', 'SE'], ['Switzerland', 'CH'], ['Syria', 'SY'], ['Taiwan', 'TW'], ['Tajikistan', 'TJ'], ['Tanzania', 'TZ'], ['Thailand', 'TH'], ['Togo', 'TG'], ['Tokelau', 'TK'], ['Tonga', 'TO'], ['Trinidad and Tobago', 'TT'], ['Tunisia', 'TN'], ['Turkey', 'TR'], ['Turkmenistan', 'TM'], ['Turks and Caicos Islands', 'TC'], ['Tuvalu', 'TV'], ['U.S. Virgin Islands', 'VI'], ['Uganda', 'UG'], ['Ukraine', 'UA'], ['United Arab Emirates', 'AE'], ['United Kingdom', 'GB'], ['United States', 'US'], ['Uruguay', 'UY'], ['Uzbekistan', 'UZ'], ['Vanuatu', 'VU'], ['Vatican', 'VA'], ['Venezuela', 'VE'], ['Vietnam', 'VN'], ['Wallis and Futuna', 'WF'], ['Western Sahara', 'EH'], ['Yemen', 'YE'], ['Zambia', 'ZM'], ['Zimbabwe', 'ZW'], ['Afghanistan', 'AF'], ['Albania', 'AL'], ['Algeria', 'DZ'], ['American Samoa', 'AS'], ['Andorra', 'AD'], ['Angola', 'AO'], ['Anguilla', 'AI'], ['Antarctica', 'AQ'], ['Antigua and Barbuda', 'AG'], ['Argentina', 'AR'], ['Armenia', 'AM'], ['Aruba', 'AW'], ['Australia', 'AU'], ['Austria', 'AT'], ['Azerbaijan', 'AZ'], ['Bahamas', 'BS'], ['Bahrain', 'BH'], ['Bangladesh', 'BD'], ['Barbados', 'BB'], ['Belarus', 'BY'], ['Belgium', 'BE'], ['Belize', 'BZ'], ['Benin', 'BJ'], ['Bermuda', 'BM'], ['Bhutan', 'BT'], ['Bolivia', 'BO'], ['Bosnia and Herzegovina', 'BA'], ['Botswana', 'BW'], ['Brazil', 'BR'], ['British Indian Ocean Territory', 'IO'], ['British Virgin Islands', 'VG'], ['Brunei', 'BN'], ['Bulgaria', 'BG'], ['Burkina Faso', 'BF'], ['Burundi', 'BI'], ['Cambodia', 'KH'], ['Cameroon', 'CM'], ['Canada', 'CA'], ['Cape Verde', 'CV'], ['Cayman Islands', 'KY'], ['Central African Republic', 'CF'], ['Chad', 'TD'], ['Chile', 'CL'], ['China', 'CN'], ['Christmas Island', 'CX'], ['Cocos Islands', 'CC'], ['Colombia', 'CO'], ['Comoros', 'KM'], ['Cook Islands', 'CK'], ['Costa Rica', 'CR'], ['Croatia', 'HR'], ['Cuba', 'CU'], ['Curacao', 'CW'], ['Cyprus', 'CY'], ['Czech Republic', 'CZ'], ['Democratic Republic of the Congo', 'CD'], ['Denmark', 'DK'], ['Djibouti', 'DJ'], ['Dominica', 'DM'], ['Dominican Republic', 'DO'], ['East Timor', 'TL'], ['Ecuador', 'EC'], ['Egypt', 'EG'], ['El Salvador', 'SV'], ['Equatorial Guinea', 'GQ'], ['Eritrea', 'ER'], ['Estonia', 'EE'], ['Ethiopia', 'ET'], ['Falkland Islands', 'FK'], ['Faroe Islands', 'FO'], ['Fiji', 'FJ'], ['Finland', 'FI'], ['France', 'FR'], ['French Polynesia', 'PF'], ['Gabon', 'GA'], ['Gambia', 'GM'], ['Georgia', 'GE'], ['Germany', 'DE'], ['Ghana', 'GH'], ['Gibraltar', 'GI'], ['Greece', 'GR'], ['Greenland', 'GL'], ['Grenada', 'GD'], ['Guam', 'GU'], ['Guatemala', 'GT'], ['Guernsey', 'GG'], ['Guinea', 'GN'], ['Guinea-Bissau', 'GW'], ['Guyana', 'GY'], ['Haiti', 'HT'], ['Honduras', 'HN'], ['Hong Kong', 'HK'], ['Hungary', 'HU'], ['Iceland', 'IS'], ['India', 'IN'], ['Indonesia', 'ID'], ['Iran', 'IR'], ['Iraq', 'IQ'], ['Ireland', 'IE'], ['Isle of Man', 'IM'], ['Israel', 'IL'], ['Italy', 'IT'], ['Ivory Coast', 'CI'], ['Jamaica', 'JM'], ['Japan', 'JP'], ['Jersey', 'JE'], ['Jordan', 'JO'], ['Kazakhstan', 'KZ'], ['Kenya', 'KE'], ['Kiribati', 'KI'], ['Kosovo', 'XK'], ['Kuwait', 'KW'], ['Kyrgyzstan', 'KG'], ['Laos', 'LA'], ['Latvia', 'LV'], ['Lebanon', 'LB'], ['Lesotho', 'LS'], ['Liberia', 'LR'], ['Libya', 'LY'], ['Liechtenstein', 'LI'], ['Lithuania', 'LT'], ['Luxembourg', 'LU'], ['Macau', 'MO'], ['Macedonia', 'MK'], ['Madagascar', 'MG'], ['Malawi', 'MW'], ['Malaysia', 'MY'], ['Maldives', 'MV'], ['Mali', 'ML'], ['Malta', 'MT'], ['Marshall Islands', 'MH'], ['Mauritania', 'MR'], ['Mauritius', 'MU'], ['Mayotte', 'YT'], ['Mexico', 'MX'], ['Micronesia', 'FM'], ['Moldova', 'MD'], ['Monaco', 'MC'], ['Mongolia', 'MN'], ['Montenegro', 'ME'], ['Montserrat', 'MS'], ['Morocco', 'MA'], ['Mozambique', 'MZ'], ['Myanmar', 'MM'], ['Namibia', 'NA'], ['Nauru', 'NR'], ['Nepal', 'NP'], ['Netherlands', 'NL'], ['Netherlands Antilles', 'AN'], ['New Caledonia', 'NC'], ['New Zealand', 'NZ'], ['Nicaragua', 'NI'], ['Niger', 'NE'], ['Nigeria', 'NG'], ['Niue', 'NU'], ['North Korea', 'KP'], ['Northern Mariana Islands', 'MP'], ['Norway', 'NO'], ['Oman', 'OM'], ['Pakistan', 'PK'], ['Palau', 'PW'], ['Palestine', 'PS'], ['Panama', 'PA'], ['Papua New Guinea', 'PG'], ['Paraguay', 'PY'], ['Peru', 'PE'], ['Philippines', 'PH'], ['Pitcairn', 'PN'], ['Poland', 'PL'], ['Portugal', 'PT'], ['Puerto Rico', 'PR'], ['Qatar', 'QA'], ['Republic of the Congo', 'CG'], ['Reunion', 'RE'], ['Romania', 'RO'], ['Russia', 'RU'], ['Rwanda', 'RW'], ['Saint Barthelemy', 'BL'], ['Saint Helena', 'SH'], ['Saint Kitts and Nevis', 'KN'], ['Saint Lucia', 'LC'], ['Saint Martin', 'MF'], ['Saint Pierre and Miquelon', 'PM'], ['Saint Vincent and the Grenadines', 'VC'], ['Samoa', 'WS'], ['San Marino', 'SM'], ['Sao Tome and Principe', 'ST'], ['Saudi Arabia', 'SA'], ['Senegal', 'SN'], ['Serbia', 'RS'], ['Seychelles', 'SC'], ['Sierra Leone', 'SL'], ['Singapore', 'SG'], ['Sint Maarten', 'SX'], ['Slovakia', 'SK'], ['Slovenia', 'SI'], ['Solomon Islands', 'SB'], ['Somalia', 'SO'], ['South Africa', 'ZA'], ['South Korea', 'KR'], ['South Sudan', 'SS'], ['Spain', 'ES'], ['Sri Lanka', 'LK'], ['Sudan', 'SD'], ['Suriname', 'SR'], ['Svalbard and Jan Mayen', 'SJ'], ['Swaziland', 'SZ'], ['Sweden', 'SE'], ['Switzerland', 'CH'], ['Syria', 'SY'], ['Taiwan', 'TW'], ['Tajikistan', 'TJ'], ['Tanzania', 'TZ'], ['Thailand', 'TH'], ['Togo', 'TG'], ['Tokelau', 'TK'], ['Tonga', 'TO'], ['Trinidad and Tobago', 'TT'], ['Tunisia', 'TN'], ['Turkey', 'TR'], ['Turkmenistan', 'TM'], ['Turks and Caicos Islands', 'TC'], ['Tuvalu', 'TV'], ['U.S. Virgin Islands', 'VI'], ['Uganda', 'UG'], ['Ukraine', 'UA'], ['United Arab Emirates', 'AE'], ['United Kingdom', 'GB'], ['United States', 'US'], ['Uruguay', 'UY'], ['Uzbekistan', 'UZ'], ['Vanuatu', 'VU'], ['Vatican', 'VA'], ['Venezuela', 'VE'], ['Vietnam', 'VN'], ['Wallis and Futuna', 'WF'], ['Western Sahara', 'EH'], ['Yemen', 'YE'], ['Zambia', 'ZM'], ['Zimbabwe', 'ZW']]
        
        for i, country in enumerate(country_mappings):
            if country[1] == patent_country_code:
                item['patent_country'] = country[0]

        ###########################
        ###OBTAIN KEY IDENTIFIER###
        ###########################

        if response.xpath('//div[@id="pagebody"]//h1/text()') != []:  
            patent_number = response.xpath('//div[@id="pagebody"]//h1/text()').re('.*?(\w{2}[0-9a-zA-Z]{0,1}\d{6}.*?\(.*?\)).*')
            pattern1 = re.match('([A-Z]{2}[0-9a-zA-Z]{0,1}\d+).*?\(([0-9a-zA-Z]{1,2})?\).*',patent_number[0]).group(1)
            pattern2 = re.match('([A-Z]{2}[0-9a-zA-Z]{0,1}\d+).*?\(([0-9a-zA-Z]{1,2})?\).*',patent_number[0]).group(2)
            patent_number = pattern1 + pattern2
            item['patent_number'] = pattern1 + pattern2
            patent_kind_code = pattern2
            item['patent_kind_code'] = pattern2
            item['key_identifier'] = patent_number
        else:
            item['patent_number'] = 'NEEDS FIXING'
            item['patent_kind_code'] = 'NEEDS FIXING!'
            item['key_identifier'] = 'NEEDS FIXING!'
            
        if response.xpath('//div[@id="pagebody"]//h3/text()') != []:
            patent_name = response.xpath('//div[@id="pagebody"]//h3/text()').extract()
            item['patent_name'] = patent_name[0].strip()
        else:
            item['patent_name'] = 'NEEDS FIXING!'

        if response.xpath('//table[@class="tableType3"]//a/text()') != []:
            bookmark0 = response.xpath('//table[@class="tableType3"]//a/text()').extract()
            bookmark0 = bookmark0[0].strip()
        else:
            bookmark0 = ''
        if response.xpath('//span[@id="bookmarkTitle"]/text()') != []:
            bookmark1 = response.xpath('//span[@id="bookmarkTitle"]/text()').extract()
            bookmark1 = bookmark1[0].strip()
        else:
            bookmark1 = ''
                          
        item['page_bookmark'] = bookmark0 + bookmark1
       
        try:
            response.xpath('//span[@id="inventors"]/text()').re('(\w+[^\n\t\r]+;?)?\\r.*')
            inventors = response.xpath('//span[@id="inventors"]/text()').re('(\w+[^\n\t\r]+;?)?\\r.*')
            inventors = [e for e in inventors if e != '']
            #item['inventors'] = ' '.join(inventors)
            item['inventors'] = inventors
        except:
            item['inventors'] = 'NEEDS FIXING!'

        try:
            response.xpath('//span[@id="applicants"]/text()').re('(\w+[^\n\t\r]+;?)?\\r.*')
            applicants = response.xpath('//span[@id="applicants"]/text()').re('(\w+[^\n\t\r]+;?)?\\r.*')
            applicants = [e for e in applicants if e != '']
            #item['applicants'] = ' '.join(applicants)
            item['applicants'] = applicants
        except:
            item['applicants'] = 'NEEDS FIXING!'

        if response.xpath('//td[@class="containsTable"]//tbody/tr[1]//a//text()') != []:
            item['classification_international'] = response.xpath('//td[@class="containsTable"]//tbody/tr[1]//a//text()').extract()
        else:
            item['classification_international'] = ''


        if response.xpath('//td[@class="containsTable"]//tbody/tr[2]//a//text()') != []:
            item['classification_cooperative'] = response.xpath('//td[@class="containsTable"]//tbody/tr[2]//a//text()').extract()
        else:
            item['classification_cooperative'] = ''


        if response.xpath('//td[@class="printTableText"]//text()') != []:
            try:
                response.xpath('//td[@class="printTableText"]//text()').re('.*?([A-Z]{2}(?:18|19|20)\d{2}[0-9A-Z]+\s*\d{8}).*')
                item['application_number'] =  response.xpath('//td[@class="printTableText"]//text()').re('.*?([A-Z]{2}(?:18|19|20)\d{2}[0-9A-Z]+\s*\d{8}).*')[0]
            except:
                item['application_number'] = ''
                
        else:
            item['application_number'] = ''

                
        
        try:
            response.xpath('//td[@class="printTableText"]//text()').re('([A-Z]{2}[0-9]+\s*\d{8})+')
            priority_numbers = response.xpath('//td[@class="printTableText"]//text()').re('([A-Z]{2}[0-9]+\s*\d{8})+')
            item['priority_numbers'] = response.xpath('//td[@class="printTableText"]//text()').re('([A-Z]{2}[0-9]+\s*\d{8})+')
        except:
            item['priority_numbers'] = ''
            

        if response.xpath('//p[@class="printAbstract"]//text()') != []:
            item['abstract'] = response.xpath('//p[@class="printAbstract"]//text()').extract()
        else:
            item['abstract'] = ''
            

        #generate next tab URL
        desc_tab = url1 + 'description' + url2

        yield Request(desc_tab, callback=self.parse_desc_tab, meta=dict(item=item))


    def parse_desc_tab(self, response):

        ##############################
        ###TAB2: Description##########
        ##############################

        #get current url, and process URL for next tab
        get = response
        url = re.match('<200\s*(.*?)>', str(get)).group(1)
        url1 = re.match('(https:\/\/worldwide\.espacenet\.com\/data\/publicationDetails\/)\w+(\?.*)',url).group(1)
        url2 = re.match('(https:\/\/worldwide\.espacenet\.com\/data\/publicationDetails\/)\w+(\?.*)',url).group(2)

        #generate next tab URL
        claims_tab = url1 + 'claims' + url2

        item = response.meta['item']

        #URL: https://worldwide.espacenet.com/publicationDetails/description?CC=US&NR=9486108B1&KC=B1&FT=D&ND=3&date=20161108&DB=EPODOC&locale=en_E
        try:
            response.xpath('//p[@class="printTableText"]//text()').extract()
            patent_description = response.xpath('//p[@class="printTableText"]//text()').extract()
            item['patent_description'] = patent_description[1:]
        except:
            item['patent_description'] = ''

        print("Testing - description tab!")

        yield Request(claims_tab, callback=self.parse_claims_tab, meta=dict(item=item))

        

    def parse_claims_tab(self, response):

        ##############################
        ###TAB3: Claims###############
        ##############################
        
        #get current url, and process URL for next tab
        get = response
        url = re.match('<200\s*(.*?)>', str(get)).group(1)
        url1 = re.match('(https:\/\/worldwide\.espacenet\.com\/data\/publicationDetails\/)\w+(\?.*)',url).group(1)
        url2 = re.match('(https:\/\/worldwide\.espacenet\.com\/data\/publicationDetails\/)\w+(\?.*)',url).group(2)

        #generate next tab URL
        cited_tab = url1 + 'citedDocuments' + url2

        item = response.meta['item']

        #URL: https://worldwide.espacenet.com/data/publicationDetails/claims?CC=US&NR=9486108B1&KC=B1&FT=D&ND=3&date=20161108&DB=EPODOC&locale=en_EP
        try:
            response.xpath('//div[@id="claims"]/p[@lang="en"]//text()').extract()
            item['original_claims'] = response.xpath('//div[@id="claims"]/p[@lang="en"]//text()').extract()
        except:
            item['original_claims'] = ''
        try:
            response.xpath('//ul[@id="claimsTree"]//text()').extract()
            item['claims_tree'] = response.xpath('//ul[@id="claimsTree"]//text()').extract()
        except:
            item['claims_tree'] = ''
        
        print("Testing - claims tab!")

        yield Request(cited_tab, callback=self.parse_cited_tab, meta=dict(item=item))



    def parse_cited_tab(self, response):

        ##############################
        ###TAB4: Cited################
        ##############################
        
        #get current url, and process URL for next tab
        get = response
        url = re.match('<200\s*(.*?)>', str(get)).group(1)
        url1 = re.match('(https:\/\/worldwide\.espacenet\.com\/data\/publicationDetails\/)\w+(\?.*)',url).group(1)
        url2 = re.match('(https:\/\/worldwide\.espacenet\.com\/data\/publicationDetails\/)\w+(\?.*)',url).group(2)

        #generate next tab URL
        citing_tab = url1 + 'citingDocuments' + url2
        
        item = response.meta['item']

        #TEST FOR TAB
        if response.xpath('//a[@class="publicationLinkClass"]').extract() != []:
            documents_cited_titles = response.xpath('//a[@class="publicationLinkClass"]').extract()
            documents_cited_titles = [BeautifulSoup(e,"lxml").findAll(text=True) for e in documents_cited_titles]
            documents_cited_titles = [e[0].strip() for e in documents_cited_titles]
            documents_cited_titles = ['Patent ' + str(int(i+1)) + ': ' + str(e) for i, e in enumerate(documents_cited_titles)]
            documents_cited_inventors = response.xpath('//td[@class="inventorColumn"]').extract()
            documents_cited_applicants = response.xpath('//td[@class="applicantColumn"]').extract()
            documents_cited_CPC = response.xpath('//td[@class="cpcColumn"]').extract()
            documents_cited_IPC = response.xpath('//div[@class="ipcColumn "]').extract()
            documents_cited_publication_info = response.xpath('//td[@class="publicationInfoColumn"]').extract()
            documents_cited_priority_date = response.xpath('//td[@class="nowrap"]').extract()
                    
            #1 process inventors
            inventors = []
            for i in range(0,len(documents_cited_inventors)):
                soup = BeautifulSoup(documents_cited_inventors[i],"lxml")
                data = soup.findAll(text=True)
                entries = ['Inventor:']
                for entry in data:
                    entry = entry.strip() + ','
                    entries.append(entry)
                entries = ' '.join(entries)
                inventors.append(entries)

            #2 process applicants
            applicants = []
            for i in range(0,len(documents_cited_applicants)):
                soup = BeautifulSoup(documents_cited_applicants[i],"lxml")
                data = soup.findAll(text=True)
                entries = ['Applicant:']
                for entry in data:
                    entry = entry.strip() + ','
                    entries.append(entry)
                entries = ' '.join(entries)
                applicants.append(entries)
            
            #3 process CPC
            CPC = []
            for i in range(0,len(documents_cited_CPC)):
                soup = BeautifulSoup(documents_cited_CPC[i],"lxml")
                data = soup.findAll(text=True)
                data = [e.strip() for e in data]
                data = [e for e in data if e != '']
                data1 = data[0]
                data2 = ', '.join(data[1:])
                data = data1 + ' ' + data2
                CPC.append(data)

            #4 process IPC
            IPC = []
            for i in range(0,len(documents_cited_IPC)):
                soup = BeautifulSoup(documents_cited_IPC[i],"lxml")
                data = soup.findAll(text=True)
                data = [e.strip() for e in data]
                data = [e for e in data if e != '']
                data1 = data[0]
                data2 = ', '.join(data[1:])
                data = data1 + ' ' + data2
                IPC.append(data)
            
            #5 process publication info
            pub_info = []
            for i in range(0,len(documents_cited_publication_info)):
                soup = BeautifulSoup(documents_cited_publication_info[i],"lxml")
                data = soup.findAll(text=True)
                data = [e.strip() for e in data]
                data = [e for e in data if e != '']
                data1 = data[0]
                data2 = ', '.join(data[1:])
                data = data1 + ' ' + data2
                pub_info.append(data)
            
            #6 process priority date
            priority_date = []
            for i in range(0,len(documents_cited_priority_date)):
                soup = BeautifulSoup(documents_cited_priority_date[i],"lxml")
                data = soup.findAll(text=True)
                data = [e.strip() for e in data]
                data = [e for e in data if e != '']
                data1 = data[0]
                data2 = ', '.join(data[1:])
                data = data1 + ' ' + data2
                priority_date.append(data)


            ###bring it all together###
            entries = []
            for i, record in enumerate(documents_cited_titles):
                entry = ''
                entry = record + ' ' + inventors[i] + ' ' + applicants[i] + ' ' + CPC[i] + ' ' + IPC[i] + ' ' + pub_info[i] + ' ' + priority_date[i] + '\n'
                entries.append(entry)
            item['cited_documents'] = entries

        else:
            item['cited_documents'] = ''

        print("Testing - cited tab!")

        
        yield Request(citing_tab, callback=self.parse_citing_tab, meta=dict(item=item))



    def parse_citing_tab(self, response):

        ##############################
        ###TAB5: Citing###############
        ##############################
        
        #get current url, and process URL for next tab
        get = response
        url = re.match('<200\s*(.*?)>', str(get)).group(1)
        url1 = re.match('(https:\/\/worldwide\.espacenet\.com\/data\/publicationDetails\/)\w+(\?.*)',url).group(1)
        url2 = re.match('(https:\/\/worldwide\.espacenet\.com\/data\/publicationDetails\/)\w+(\?.*)',url).group(2)

        #generate next tab URL
        inpadoc_tab = url1 + 'inpadoc' + url2
        
        item = response.meta['item']

        #TEST TAB
        if response.xpath('//a[@class="publicationLinkClass"]').extract() != []:
            documents_citing_titles = response.xpath('//a[@class="publicationLinkClass"]').extract()
            documents_citing_titles = [BeautifulSoup(e,"lxml").findAll(text=True) for e in documents_citing_titles]
            documents_citing_titles = [e[0].strip() for e in documents_citing_titles]
            documents_citing_titles = ['Patent ' + str(int(i+1)) + ': ' + str(e) for i, e in enumerate(documents_citing_titles)]
            documents_citing_inventors = response.xpath('//td[@class="inventorColumn"]').extract()
            documents_citing_applicants = response.xpath('//td[@class="applicantColumn"]').extract()
            documents_citing_CPC = response.xpath('//td[@class="cpcColumn"]').extract()
            documents_citing_IPC = response.xpath('//div[@class="ipcColumn "]').extract()
            documents_citing_publication_info = response.xpath('//td[@class="publicationInfoColumn"]').extract()
            documents_citing_priority_date = response.xpath('//td[@class="nowrap"]').extract()
                    
            #1 process inventors
            inventors = []
            for i in range(0,len(documents_citing_inventors)):
                soup = BeautifulSoup(documents_citing_inventors[i],"lxml")
                data = soup.findAll(text=True)
                entries = ['Inventor:']
                for entry in data:
                    entry = entry.strip() + ','
                    entries.append(entry)
                entries = ' '.join(entries)
                inventors.append(entries)

            #2 process applicants
            applicants = []
            for i in range(0,len(documents_citing_applicants)):
                soup = BeautifulSoup(documents_citing_applicants[i],"lxml")
                data = soup.findAll(text=True)
                entries = ['Applicant:']
                for entry in data:
                    entry = entry.strip() + ','
                    entries.append(entry)
                entries = ' '.join(entries)
                applicants.append(entries)
            
            #3 process CPC
            CPC = []
            for i in range(0,len(documents_citing_CPC)):
                soup = BeautifulSoup(documents_citing_CPC[i],"lxml")
                data = soup.findAll(text=True)
                data = [e.strip() for e in data]
                data = [e for e in data if e != '']
                data1 = data[0]
                data2 = ', '.join(data[1:])
                data = data1 + ' ' + data2
                CPC.append(data)

            #4 process IPC
            IPC = []
            for i in range(0,len(documents_citing_IPC)):
                soup = BeautifulSoup(documents_citing_IPC[i],"lxml")
                data = soup.findAll(text=True)
                data = [e.strip() for e in data]
                data = [e for e in data if e != '']
                data1 = data[0]
                data2 = ', '.join(data[1:])
                data = data1 + ' ' + data2
                IPC.append(data)
            
            #5 process publication info
            pub_info = []
            for i in range(0,len(documents_citing_publication_info)):
                soup = BeautifulSoup(documents_citing_publication_info[i],"lxml")
                data = soup.findAll(text=True)
                data = [e.strip() for e in data]
                data = [e for e in data if e != '']
                data1 = data[0]
                data2 = ', '.join(data[1:])
                data = data1 + ' ' + data2
                pub_info.append(data)
            
            #6 process priority date
            priority_date = []
            for i in range(0,len(documents_citing_priority_date)):
                soup = BeautifulSoup(documents_citing_priority_date[i],"lxml")
                data = soup.findAll(text=True)
                data = [e.strip() for e in data]
                data = [e for e in data if e != '']
                data1 = data[0]
                data2 = ', '.join(data[1:])
                data = data1 + ' ' + data2
                priority_date.append(data)


            ###bring it all together###
            entries = []
            for i, record in enumerate(documents_citing_titles):
                entry = ''
                entry = record + ' ' + inventors[i] + ' ' + applicants[i] + ' ' + CPC[i] + ' ' + IPC[i] + ' ' + pub_info[i] + ' ' + priority_date[i] + '\n'
                entries.append(entry)
            item['citing_documents'] = entries

        else:
            item['citing_documents'] = ''

        print("Testing - citing tab!")

        yield Request(inpadoc_tab, callback=self.parse_inpadoc_tab, meta=dict(item=item))



    def parse_inpadoc_tab(self, response):

        ##############################
        ###TAB6: INPADOC##############
        ##############################
        
        #get current url, and process URL for next tab
        get = response
        url = re.match('<200\s*(.*?)>', str(get)).group(1)
        url1 = re.match('(https:\/\/worldwide\.espacenet\.com\/data\/publicationDetails\/)\w+(\?.*)',url).group(1)
        url2 = re.match('(https:\/\/worldwide\.espacenet\.com\/data\/publicationDetails\/)\w+(\?.*)',url).group(2)
        
        #generate next tab URL
        inpadoc_patent_family_tab = url1 + 'inpadocPatentFamily' + url2

        item = response.meta['item']

        #TEST TAB
        if response.xpath('//div[@name="loadingDiv"]//tr').extract() != []:
            inpadoc = ''
            inpadoc_data = response.xpath('//div[@name="loadingDiv"]//tr').extract()
            for i in range(0,len(inpadoc_data)):
                soup = BeautifulSoup(inpadoc_data[i],"lxml")
                data = soup.findAll(text=True)
                data = [e.strip() for e in data]
                data = [e for e in data if e != '']
                data = [e.replace('\n','') for e in data]
                data = [e.replace('\t','') for e in data]
                data = ''.join(data)
                inpadoc = inpadoc + str(data) + '\n'
                print(inpadoc)

            item['INPADOC_legal_status'] = inpadoc

        else:
            item['INPADOC_legal_status'] = ''

        print("Testing - inpadoc tab!")

        yield Request(inpadoc_patent_family_tab, callback=self.parse_inpadoc_patent_family_tab, meta=dict(item=item))



    def parse_inpadoc_patent_family_tab(self, response):

        #################################
        ###TAB7: INPADOC patent family###
        #################################
        
        
        #get current url, and process URL for next tab
        get = response
        url = re.match('<200\s*(.*?)>', str(get)).group(1)
        url1 = re.match('(https:\/\/worldwide\.espacenet\.com\/data\/publicationDetails\/)\w+(\?.*)',url).group(1)
        url2 = re.match('(https:\/\/worldwide\.espacenet\.com\/data\/publicationDetails\/)\w+(\?.*)',url).group(2)
        
        item = response.meta['item']

        #TEST TAB
        if response.xpath('//a[@class="publicationLinkClass"]').extract() != []:
            INPADOC_patent_family_titles = response.xpath('//a[@class="publicationLinkClass"]').extract()
            INPADOC_patent_family_titles = [BeautifulSoup(e,"lxml").findAll(text=True) for e in INPADOC_patent_family_titles]
            INPADOC_patent_family_titles = [e[0].strip() for e in INPADOC_patent_family_titles]
            INPADOC_patent_family_titles = ['Patent ' + str(int(i+1)) + ': ' + str(e) for i, e in enumerate(INPADOC_patent_family_titles)]
            INPADOC_patent_family_inventors = response.xpath('//td[@class="inventorColumn"]').extract()
            INPADOC_patent_family_applicants = response.xpath('//td[@class="applicantColumn"]').extract()
            INPADOC_patent_family_CPC = response.xpath('//td[@class="cpcColumn"]').extract()
            INPADOC_patent_family_IPC = response.xpath('//div[@class="ipcColumn "]').extract()
            INPADOC_patent_family_publication_info = response.xpath('//td[@class="publicationInfoColumn"]').extract()
            INPADOC_patent_family_priority_date = response.xpath('//td[@class="nowrap"]').extract()
                    
            #1 process inventors
            inventors = []
            for i in range(0,len(INPADOC_patent_family_inventors)):
                soup = BeautifulSoup(INPADOC_patent_family_inventors[i],"lxml")
                data = soup.findAll(text=True)
                entries = ['Inventor:']
                for entry in data:
                    entry = entry.strip() + ','
                    entries.append(entry)
                entries = ' '.join(entries)
                inventors.append(entries)

            #2 process applicants
            applicants = []
            for i in range(0,len(INPADOC_patent_family_applicants)):
                soup = BeautifulSoup(INPADOC_patent_family_applicants[i],"lxml")
                data = soup.findAll(text=True)
                entries = ['Applicant:']
                for entry in data:
                    entry = entry.strip() + ','
                    entries.append(entry)
                entries = ' '.join(entries)
                applicants.append(entries)
            
            #3 process CPC
            CPC = []
            for i in range(0,len(INPADOC_patent_family_CPC)):
                soup = BeautifulSoup(INPADOC_patent_family_CPC[i],"lxml")
                data = soup.findAll(text=True)
                data = [e.strip() for e in data]
                data = [e for e in data if e != '']
                data1 = data[0]
                data2 = ', '.join(data[1:])
                data = data1 + ' ' + data2
                CPC.append(data)

            #4 process IPC
            IPC = []
            for i in range(0,len(INPADOC_patent_family_IPC)):
                soup = BeautifulSoup(INPADOC_patent_family_IPC[i],"lxml")
                data = soup.findAll(text=True)
                data = [e.strip() for e in data]
                data = [e for e in data if e != '']
                data1 = data[0]
                data2 = ', '.join(data[1:])
                data = data1 + ' ' + data2
                IPC.append(data)
            
            #5 process publication info
            pub_info = []
            for i in range(0,len(INPADOC_patent_family_publication_info)):
                soup = BeautifulSoup(INPADOC_patent_family_publication_info[i],"lxml")
                data = soup.findAll(text=True)
                data = [e.strip() for e in data]
                data = [e for e in data if e != '']
                data1 = data[0]
                data2 = ', '.join(data[1:])
                data = data1 + ' ' + data2
                pub_info.append(data)
            
            #6 process priority date
            priority_date = []
            for i in range(0,len(INPADOC_patent_family_priority_date)):
                soup = BeautifulSoup(INPADOC_patent_family_priority_date[i],"lxml")
                data = soup.findAll(text=True)
                data = [e.strip() for e in data]
                data = [e for e in data if e != '']
                data1 = data[0]
                data2 = ', '.join(data[1:])
                data = data1 + ' ' + data2
                priority_date.append(data)

            ###bring it all together###
            entries = []
            for i, record in enumerate(INPADOC_patent_family_titles):
                entry = ''
                entry = record + ' ' + inventors[i] + ' ' + applicants[i] + ' ' + CPC[i] + ' ' + IPC[i] + ' ' + pub_info[i] + ' ' + priority_date[i] + '\n'
                entries.append(entry)
            item['INPADOC_patent_family'] = entries

        else:
            item['INPADOC_patent_family'] = ''


        print("Testing - inpadoc Patent Family tab!")


        yield item

#scrapy crawl espacenet_europe -o espacenet_europe_test1.csv
