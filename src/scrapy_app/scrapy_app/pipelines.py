# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from notifications.models import Item
import json
import logging

class ScrapyAppPipeline(object):
    def __init__(self, unique_id, *args, **kwargs):
        self.unique_id = unique_id
        self.items = []

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            unique_id=crawler.settings.get('unique_id')
        )

    def close_spider(self, spider):
        item = Item()
        item.unique_id = self.unique_id
        item.data = json.dumps(self.items)
        item.save()

    def process_item(self, item, spider):
        print('Url: ', item)
        self.items.append(item['url'])
        return item
