# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class EmailsItem(Item):
    # define the fields for your item here like:
	name = Field()
	subject = Field()
	date_time = Field()
	email_body = Field()
	topic = Field()
