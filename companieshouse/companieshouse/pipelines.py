# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
import time
from random import randint
from time import sleep
from scrapy import signals
from scrapy.exporters import CsvItemExporter


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
      if num % 1000 == 0:
        t = 900
        for i in xrange(t,0,-1):
          time.sleep(1)
          sys.stdout.write(str(i)+' ')
          sys.stdout.flush()
      elif num % 100 == 0:
        t = randint(1,60)
        for i in xrange(t,0,-1):
          time.sleep(1)
          sys.stdout.write(str(i)+' ')
          sys.stdout.flush()

    return item


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
    file = open('%s_items_test6.csv' % spider.name, 'w+b')
    self.files[spider] = file
    self.exporter = CsvItemExporter(file)
    self.exporter.fields_to_export = ['company_name', 'company_address', 'company_status', 'company_type', 'company_number', 'officer1_first_names', 'officer1_last_name', 'officer2_first_names', 'officer2_last_name', 'officer3_first_names', 'officer3_last_name', 'officer4_first_names', 'officer4_last_name', 'officer5_first_names', 'officer5_last_name', 'officer6_first_names', 'officer6_last_name', 'officer7_first_names', 'officer7_last_name', 'officer8_first_names', 'officer8_last_name', 'officer9_first_names', 'officer9_last_name', 'officer10_first_names', 'officer10_last_name', 'officer11_first_names', 'officer11_last_name', 'officer12_first_names', 'officer12_last_name', 'officer13_first_names', 'officer13_last_name', 'officer14_first_names', 'officer14_last_name', 'officer15_first_names', 'officer15_last_name', 'officer16_first_names', 'officer16_last_name', 'officer17_first_names', 'officer17_last_name', 'officer18_first_names', 'officer18_last_name', 'officer19_first_names', 'officer19_last_name', 'officer20_first_names', 'officer20_last_name', 'officer1_occupation', 'officer2_occupation', 'officer3_occupation', 'officer4_occupation', 'officer5_occupation', 'officer6_occupation', 'officer7_occupation', 'officer8_occupation', 'officer9_occupation', 'officer10_occupation', 'officer11_occupation', 'officer12_occupation', 'officer13_occupation', 'officer14_occupation', 'officer15_occupation', 'officer16_occupation', 'officer17_occupation', 'officer18_occupation', 'officer19_occupation', 'officer20_occupation', 'officer1_status', 'officer2_status', 'officer3_status', 'officer4_status', 'officer5_status', 'officer6_status', 'officer7_status', 'officer8_status', 'officer9_status', 'officer10_status', 'officer11_status', 'officer12_status', 'officer13_status', 'officer14_status', 'officer15_status', 'officer16_status', 'officer17_status', 'officer18_status', 'officer19_status', 'officer20_status', 'nature_of_business', 'officers_url']
    self.exporter.start_exporting()

  def spider_closed(self, spider):
    self.exporter.finish_exporting()
    file = self.files.pop(spider)
    file.close()

  def process_item(self, item, spider):
    self.exporter.export_item(item)
    return item
