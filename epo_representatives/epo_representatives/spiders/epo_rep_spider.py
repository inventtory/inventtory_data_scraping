'''
    File name: epo_rep_spider.py
    Author: Seraphina Anderson
    Date last modified: 12/1/2017
    Python Version: 2.7
'''


# -*- coding: utf-8 -*-

import scrapy
import re
import json
import csv
import urllib
import requests
from bs4 import BeautifulSoup
from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from epo_representatives.items import EpoRepresentativesItem



class EpoRepSpider(CrawlSpider):
    
    name = "epo_rep"
    
    #1
    def start_requests(self):
        print("testing #1")
        start_url = 'https://forms.epo.org/app2/service/profRep.php?get=countries&format=json&sort=name&language=en'
        yield Request(start_url, callback=self.parse_start_url, dont_filter=True)

    #2
    def parse_start_url(self, response):
        print("testing #2")
        get = response
        url = re.match('<200\s*(.*?)>', str(get)).group(1)
        #process json and generate url for each country listed
        data = json.loads(response.body_as_unicode())
        for i in range(1,len(data)):
            item = EpoRepresentativesItem()
            iso = data[i]['iso']
            country_name = data[i]['name']
            item['iso'] = iso
            item['no_hits'] = data[i]['count']
            item['country_name'] = data[i]['name']
            #generate country url
            country_url = 'https://forms.epo.org/app2/service/profRep.php?get=query&format=json&perPage=100&pageId=1&countryId=' + str(iso)
            item['iter1'] = i
            yield Request(country_url, callback=self.parse_country_url, meta=dict(item=item), dont_filter=True, priority = 1)

    #3
    def parse_country_url(self, response):
        print("testing #3")
        ## get URL ##
        get = response
        url = re.match('<200\s*(.*?)>', str(get)).group(1)
        data = json.loads(response.body_as_unicode())

        ###get number of items

        #################
        ###paging info###
        #################

        pages = int(data["pagingInfo"]["pages"])

        for j in range(1,pages+1):
            item = response.meta['item']
            part1 = re.match('(.*?pageId=)\d+(.*)',url).group(1)
            part2 = re.match('(.*?pageId=)\d+(.*)',url).group(2)
            country_page = part1 + str(j) + part2
            yield Request(country_page, callback=self.parse_country_page, meta=dict(item=item), dont_filter=True)


    #4
    def parse_country_page(self, response):
        print("testing #4")
        ## get URL ##
        get = response
        url = re.match('<200\s*(.*?)>', str(get)).group(1)
        data = json.loads(response.body_as_unicode())
        
        for k in range(0,len(data['resultList'])):
            
            ##########
            ###meta###
            ##########
            
            item = response.meta['item']
            
            if data["pagingInfo"]["nRecs"] is not None:
                item['n_recs'] = data["pagingInfo"]["nRecs"]
            else:
                item['n_recs'] = ''
            if data["pagingInfo"]["pageId"] is not None:
                item['page_Id'] = data["pagingInfo"]["pageId"]
            else:
                item['page_Id'] = ''
            if data["pagingInfo"]["pages"] is not None:
                item['pages'] = data["pagingInfo"]["pages"]
            else:
                item['pages'] = ''
                

            ############
            ###params###
            ############
            if data["pagingInfo"]["params"]["city"] is not None:
                item['city'] = data["pagingInfo"]["params"]["city"]
            else:
                item['city'] = ''
            if data["pagingInfo"]["params"]["perPage"] is not None:
                item['per_page'] = data["pagingInfo"]["params"]["perPage"]
            else:
                item['per_page'] = ''
            if data["pagingInfo"]["params"]["countryId"] is not None:
                item['country_id_1'] = data["pagingInfo"]["params"]["countryId"]
            else:
                item['country_id_1'] = ''
            if data["pagingInfo"]["params"]["countryId2"] is not None:
                item['country_id_2'] = data["pagingInfo"]["params"]["countryId2"]
            else:
                item['country_id_2'] = ''
            if data["pagingInfo"]["params"]["name"] is not None:
                item['name'] = data["pagingInfo"]["params"]["name"]
            else:
                item['name'] = ''
            if data["pagingInfo"]["params"]["format"] is not None:
                item['data_format'] = data["pagingInfo"]["params"]["format"]
            else:
                item['data_format'] = ''
            if data["pagingInfo"]["params"]["module"] is not None:
                item['module'] = data["pagingInfo"]["params"]["module"]
            else:
                item['module'] = ''
            if data["pagingInfo"]["params"]["callback"] is not None:
                item['callback'] = data["pagingInfo"]["params"]["callback"]
            else:
                item['callback'] = ''
            if data["pagingInfo"]["params"]["postCode"] is not None:
                item['post_code'] = data["pagingInfo"]["params"]["postCode"]
            else:
                item['post_code'] = ''
            if data["pagingInfo"]["params"]["pane"] is not None:
                item['pane'] = data["pagingInfo"]["params"]["pane"]
            else:
                item['pane'] = ''
            if data["pagingInfo"]["params"]["pg"] is not None:
                item['pg'] = data["pagingInfo"]["params"]["pg"]
            else:
                item['pg'] = ''
            if data["pagingInfo"]["params"]["nr"] is not None:
                item['nr'] = data["pagingInfo"]["params"]["nr"]
            else:
                item['nr'] = ''

            
            ###############
            ###main data###
            ###############
            if data['resultList'][k]['postcode'] is not None:
                item['postcode'] = data['resultList'][k]['postcode']
            else:
                item['postcode'] = ''
            if data['resultList'][k]['id'] is not None:
                item['company_id'] = data['resultList'][k]['id']
            else:
                item['company_id'] = ''
            if data['resultList'][k]['strasse1'] is not None:
                item['strasse1'] = data['resultList'][k]['strasse1']
            else:
                item['strasse1']
            if data['resultList'][k]['strasse2'] is not None:
                item['strasse2'] = data['resultList'][k]['strasse2']
            else:
                item['strasse2'] = ''
            if data['resultList'][k]['strasse3'] is not None:
                item['strasse3'] = data['resultList'][k]['strasse3']
            else:
                item['strasse3'] = ''
            if data['resultList'][k]['strasse4'] is not None:
                item['strasse4'] = data['resultList'][k]['strasse4']
            else:
                item['strasse4'] = ''
            if data['resultList'][k]['telefax'] is not None:
                item['telefax1'] = data['resultList'][k]['telefax']
            else:
                item['telefax1'] = ''
            if data['resultList'][k]['telefax2'] is not None:
                item['telefax2'] = data['resultList'][k]['telefax2']
            else:
                item['telefax2'] = ''
            if data['resultList'][k]['email'] is not None:
                item['email'] = data['resultList'][k]['email']
            else:
                item['email'] = ''
            if data['resultList'][k]['sCity'] is not None:
                item['s_city'] = data['resultList'][k]['sCity']
            else:
                item['s_city'] = ''
            if data['resultList'][k]['land'] is not None:
                item['land1'] = data['resultList'][k]['land']
            else:
                item['land1'] = ''
            if data['resultList'][k]['land2'] is not None:
                item['land2'] = data['resultList'][k]['land2']
            else:
                item['land2'] = ''
            if data['resultList'][k]['postcodelr'] is not None:
                item['postcodelr'] = data['resultList'][k]['postcodelr']
            else:
                item['postcodelr'] = ''
            if data['resultList'][k]['ort'] is not None:
                item['ort'] = data['resultList'][k]['ort']
            else:
                item['ort'] = ''
            if data['resultList'][k]['tel1'] is not None:
                item['tel1'] = data['resultList'][k]['tel1']
            else:
                item['tel1'] = ''
            if data['resultList'][k]['tel2'] is not None:
                item['tel2'] = data['resultList'][k]['tel2']
            else:
                item['tel2'] = ''
            if data['resultList'][k]['name1'] is not None:
                full_name = data['resultList'][k]['name1']
                full_name = full_name.split(',')
                item['first_names'] = full_name[1]
                item['last_name'] = full_name[0]
            else:
                item['first_names'] = full_name[1]
                item['last_name'] = full_name[0]
            if data['resultList'][k]['url'] is not None:
                item['url'] = data['resultList'][k]['url']
            else:
                item['url'] = ''
            if data['resultList'][k]['telex'] is not None:
                item['telex'] = data['resultList'][k]['telex']
            else:
                item['telex'] = ''
                
            item['page_url'] = url #url being scraped
            item['iter2'] = data["pagingInfo"]["pageId"] #current page number
            item['iter3'] = k+1 #this is item number
 
            yield item

#to output to csv: scrapy crawl epo_rep -o epo_rep.csv
#no of data entries as of 11/1/2017 is 11749






            
