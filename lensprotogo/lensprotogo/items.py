# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Webscrapycam(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    image_url = scrapy.Field()
    price = scrapy.Field()
    product_link = scrapy.Field()
    product_location = scrapy.Field()

class Webscrapylense(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    image_url = scrapy.Field()
    price = scrapy.Field()
    product_link = scrapy.Field()
    product_location = scrapy.Field()