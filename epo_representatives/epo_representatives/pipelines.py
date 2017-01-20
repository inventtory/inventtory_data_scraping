# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
from scrapy.exporters import CsvItemExporter

##class EpoRepresentativesPipeline(object):
##    def process_item(self, item, spider):
##        return item

class CSVPipeline(object):

  def __init__(self):
    self.files = {}

  @classmethod
  def from_crawler(cls, crawler):
    pipeline = cls()
    crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
    crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
    return pipeline

  def spider_opened(self, spider):
    file = open('%s_items_2.csv' % spider.name, 'w+b')
    self.files[spider] = file
    self.exporter = CsvItemExporter(file)
    self.exporter.fields_to_export = ['iter1', 'iter2', 'iter3', 'page_url', 'no_hits', 'iso', 'country_name', 'paging_info', 'params', 'n_recs', 'page_Id', 'pages', 'city', 'per_page', 'country_id_1', 'country_id_2', 'name', 'data_format', 'module', 'callback', 'post_code', 'pane', 'pg', 'nr', 'postcode', 'company_id', 'company_name', 'strasse1', 'strasse2', 'strasse3', 'strasse4', 'telefax1', 'telefax2', 'email', 's_city', 'land1', 'land2', 'postcodelr', 'ort', 'tel1', 'tel2', 'first_names', 'last_name', 'url', 'telex']
    self.exporter.start_exporting()

  def spider_closed(self, spider):
    self.exporter.finish_exporting()
    file = self.files.pop(spider)
    file.close()

  def process_item(self, item, spider):
    self.exporter.export_item(item)
    return item
