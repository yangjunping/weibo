# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from weibo.items import WeiboItem

class WeiboPipeline(object):
    def __init__(self):
        self.client=pymongo.MongoClient(host="localhost",port=27017)
        self.db=self.client.yang
        self.collection=self.db.weibo
    def process_item(self, item, spider):
        print("--------------------")
        print(item)
        print("--------------------")
        self.collection.insert(dict(item))
        return item
