# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class MetaDataItem(scrapy.Item):
    #test data structure
    iter1 = scrapy.Field()
    iter2 = scrapy.Field()
    iter3 = scrapy.Field()
    page_url = scrapy.Field()
    
class EpoRepresentativesItem(scrapy.Item):
    #test data structure
    iter1 = scrapy.Field()
    iter2 = scrapy.Field()
    iter3 = scrapy.Field()
    page_url = scrapy.Field()

    #paging info
    no_hits = scrapy.Field()
    iso = scrapy.Field()
    country_name = scrapy.Field()
    paging_info = scrapy.Field()
    params = scrapy.Field()
    n_recs = scrapy.Field()
    page_Id = scrapy.Field()
    pages = scrapy.Field()

    #params
    city = scrapy.Field()
    per_page = scrapy.Field()
    country_id_1 = scrapy.Field()
    country_id_2 = scrapy.Field()
    name = scrapy.Field()
    data_format = scrapy.Field()
    module = scrapy.Field()
    callback = scrapy.Field()
    post_code = scrapy.Field()
    pane = scrapy.Field()
    pg = scrapy.Field()
    nr = scrapy.Field()

    # main data
    postcode = scrapy.Field()
    company_id = scrapy.Field()
    company_name = scrapy.Field()
    strasse1 = scrapy.Field()
    strasse2 = scrapy.Field()
    strasse3 = scrapy.Field()
    strasse4 = scrapy.Field()
    telefax1 = scrapy.Field()
    telefax2 = scrapy.Field()
    email = scrapy.Field()
    s_city = scrapy.Field()
    land1 = scrapy.Field()
    land2 = scrapy.Field()
    postcodelr = scrapy.Field()
    ort = scrapy.Field()
    tel1 = scrapy.Field()
    tel2 = scrapy.Field()
    first_names = scrapy.Field()
    last_name = scrapy.Field()
    url = scrapy.Field()
    telex = scrapy.Field()
