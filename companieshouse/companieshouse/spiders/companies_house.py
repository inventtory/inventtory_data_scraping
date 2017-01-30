'''
    File name: companies_house.py
    Author: Seraphina Anderson
    Date last modified: 23/1/2017
    Python Version: 2.7, 3.5
'''


# -*- coding: utf-8 -*-

import scrapy
import re
import json
import csv
import urllib
import requests
import sys
import time
from random import randint
from time import sleep
from bs4 import BeautifulSoup
from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from companieshouse.items import CompanieshouseItem



class CompaniesHouseSpider(CrawlSpider):
    
    name = "companies_house"
    
    #1
    def start_requests(self):
        alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '!', '"', '\xa3', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+', '=', '<', '>', '?', ',', '.', '/', '@', '~', ':', "'", '#', '~', '|', '\\', '{', '}', '[', ']']
        print("testing #1")
        for i, letter in enumerate(alpha):
            start_url = 'https://beta.companieshouse.gov.uk/search/companies?q=' + str(letter)
            yield Request(start_url, callback=self.parse_start_url)

    #2
    def parse_start_url(self, response):
        print("testing #2")
        url = response.url
        #get total number of pages
        matches = response.xpath('//div[@id="search-meta"]//text()').re('.*?of\s*(\d+)')[0]
        #generate pages
        for i in range(1,21):
            page = url + '&page=' + str(i)
            yield Request(page, callback=self.parse_page)

    #3
    def parse_page(self, response):
        print("testing #3")
        url = response.url
        company_links = response.xpath('//ul[@id="results"]/li/h3/a/@href').extract()
        company_links = ['https://beta.companieshouse.gov.uk' + str(e) for e in company_links]
        for link in company_links:
            yield Request(link, callback=self.parse_company_link)

    #4
    def parse_company_link(self, response):
        print("testing #4")
        url = response.url

        item = CompanieshouseItem()

        ###test criteria: "Company Type = private limited company", "Status=Active", "Nature of business = ???###
        if response.xpath('//dd[@id="company-status"]/text()').extract() != []:
            if response.xpath('//dd[@id="company-status"]/text()').extract()[0].strip() == "Active":
                if response.xpath('//dd[@id="company-type"]/text()').extract() != []:
                    if response.xpath('//dd[@id="company-type"]/text()').extract()[0].strip() == "Private limited Company":
                        ###get data###
                        item['company_status'] = response.xpath('//dd[@id="company-status"]/text()').extract()[0].strip()
                        item['company_type'] = response.xpath('//dd[@id="company-type"]/text()').extract()[0].strip()
                        try: 
                            item['company_number'] = re.match('.*company.([0-9A-Z]{8}).*',url).group(1)
                        except:
                            print("url: ",url)
                            item['company_number'] = ''
                        if response.xpath('//p[@id="company-name"]/text()').extract() != []:
                            item['company_name'] =  response.xpath('//p[@id="company-name"]/text()').extract()[0].strip()
                        else:
                            item['company_name'] = ''
                        if response.xpath('//*[@id="content-container"]/dl/dd/text()').extract() != []:
                            item['company_address'] = response.xpath('//*[@id="content-container"]/dl/dd/text()').extract()[0].strip()
                        else:
                            item['company_address'] = ''
                        try:
                            item['nature_of_business'] = response.xpath('//span[contains(@id, "sic")]/text()').extract()[0].strip()
                        except:
                            item['nature_of_business'] = ''
                            
                        ###get link to officer data###
                        officer_link = url + '/officers'
                        
                        yield Request(officer_link, callback=self.parse_people, meta=dict(item=item))
        
        else:
            pass

    #5
    def parse_people(self, response):
        print("testing #5")

        item = response.meta['item']

        ###get officer data###

        officer_names = response.xpath('//span[contains(@id, "officer-name-")]//text()').extract()
        officer_names = [e.split(',') for e in officer_names if '\n' not in e]
        status = response.xpath('//span[contains(@id, "officer-status-tag-")]/text()').extract()
        officer_occupations = response.xpath('//dd[contains(@id, "officer-role-")]/text()').extract()
        officer_occupations = [e.strip() for e in officer_occupations]
        data = response.xpath('//div[contains(@class, "appointment-")]').extract()


        for i in range(0,len(officer_names)):

            item['officers_url'] = response.url

            index = i + 1
            
            if "Resigned" in data[i]:
                pass
            else:
                if "Active" in data[i]:
                    item['officer%d_status' % index] = "Active"
                else:
                    item['officer%d_status' % index] = "Active"
                try:
                    item['officer%d_first_names' % index] = officer_names[i][1]
                except:
                    item['officer%d_first_names' % index] = officer_names[i]
                try:
                    item['officer%d_last_name' % index] = officer_names[i][0]
                except:
                    item['officer%d_last_name' % index] = officer_names[i]
                item['officer%d_occupation' % index] = officer_occupations[i]

        yield item

                
                    

        #scrapy crawl comp_house -o comp_house_test1.csv 
