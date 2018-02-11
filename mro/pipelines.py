# -*- coding: utf-8 -*-
from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter
from mro.BaseSpiders.base_spiders import BaseMroSpider


class MroPipeline(object):
  def __init__(self):
    self.files = {}

  @classmethod
  def from_crawler(cls, crawler):
    if BaseMroSpider not in crawler.spider.__class__.__bases__:
        return None
    pipeline = cls()
    crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
    crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
    return pipeline

  def spider_opened(self, spider):
    file = open(getattr(spider, 'output_filename', 'result_{}.csv'.format(spider.name)), 'w+b')
    self.files[spider] = file
    self.exporter = CsvItemExporter(file)
    self.exporter.fields_to_export = getattr(spider, 'output_fields', None)
    self.exporter.start_exporting()

  def spider_closed(self, spider):
    self.exporter.finish_exporting()
    file = self.files.pop(spider)
    file.close()

  def process_item(self, item, spider):
    self.exporter.export_item(item)
    return item
