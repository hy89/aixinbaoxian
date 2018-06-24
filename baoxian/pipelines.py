# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient


class BaoxianPipeline(object):
    def open_spider(self, spider):
        client = MongoClient()
        self.collection = client.baoxian.agent

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

