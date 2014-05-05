# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request


class GommadirettoPipeline(object):
    def process_item(self, item, spider):
    	item['image_paths'] = item['images'][0]['path'] 
        return item

