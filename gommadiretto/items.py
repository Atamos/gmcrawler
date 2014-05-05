# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.contrib.loader.processor import MapCompose, Join, TakeFirst
from scrapy.utils.markup import remove_entities
from scrapy import log


def filter_price(value):
	if value.isdigit():
		return value

def filter_ttype(value):
	return "marco"

def filter_word(v):
	v.replace(',','')
	v.replace('-','')
	return v

def filter_br(v):
	v2 = v.replace('<br>',"\r\n")
	v2 = v2.replace('<p>','')
	v2 = v2.replace('<b>','')
	v2 = v2.replace('<i>','')
	v2 = v2.replace('</p>','')
	v2 = v2.replace('</b>','')
	v2 = v2.replace('</i>','')
	return v2


class GommadirettoItem(Item):
    # define the fields for your item here like:
    # name = Field()
    title = Field()
    name = Field()
    disponibility = Field()
    ttype = Field()
    iv = Field(
    	input_processor=MapCompose(filter_word),
    	output_processor=Join()
    )
    size = Field()
    ue = Field(
    	input_processor=MapCompose(unicode.strip,filter_word),
    	output_processor=Join()
    )
    small = Field(
    	input_processor=MapCompose(unicode.strip,filter_word),
    	output_processor=Join()
    )
    tlong = Field(
    	input_processor=MapCompose(unicode.strip,filter_br,remove_entities),
    	output_procesor=Join("\n")
    )
    price = Field(
    	input_processor=MapCompose(remove_entities),
        output_processor=TakeFirst(),
   	)
    link = Field()
    image_urls = Field()
    images = Field()
    image_paths = Field()


