# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from itemadapter import ItemAdapter

class ParseCategory(object):
    def process_item(self, item, spider):
      
        data = item['link'].split('/')
        item['category'] = data[3]
        
        return item

class CleanData(object):
    # Remove \t\r\n
    def process_item(self, item, spider):
        for field in ['title', 'text', 'created_at']:
          # try:
          item[field] = item[field].replace('\t', ' ')
          item[field] = item[field].replace('\r', ' ')
          item[field] = item[field].replace('\n', ' ')
          item[field] = item[field].strip()
          # except:
            # pass
        return item
      
class SaveItem(object):

    def open_spider(self, spider):
      self.file = open('notices.json', 'w')

    def close_spider(self, spider):
      self.file.close()

    def process_item(self, item, spider):
      # line =  json.dumps(dict(item)) + '\n'
      line = json.dumps(ItemAdapter(item).asdict()) + "\n"
      self.file.write(line)
      return item