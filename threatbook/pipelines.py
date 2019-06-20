# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class ThreatbookPipeline(object):
    def process_item(self, item, spider):
        spider.r.sadd("threatbook:threat", json.dumps(dict(item), ensure_ascii=False))
        return item
