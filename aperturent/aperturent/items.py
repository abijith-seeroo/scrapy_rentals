# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WebscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()

class WebscrapyCamera(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    price = scrapy.Field()
    image_url = scrapy.Field()
    product_link = scrapy.Field()
    product_location = scrapy.Field()

class WebscrapyLens(scrapy.Item):
    # define the fields for your item here like:
    product_name = scrapy.Field()
    product_desc = scrapy.Field()
    product_image = scrapy.Field()
    product_see_more = scrapy.Field()

class Webscrapylight(scrapy.Item):
    # define the fields for your item here like:
    product_name = scrapy.Field()
    product_desc = scrapy.Field()
    product_image = scrapy.Field()
    product_see_more = scrapy.Field()

class Webscrapyvideo(scrapy.Item):
    # define the fields for your item here like:
    product_name = scrapy.Field()
    product_desc = scrapy.Field()
    product_image = scrapy.Field()
    product_see_more = scrapy.Field()

class Webscrapyaccess(scrapy.Item):
    # define the fields for your item here like:
    product_name = scrapy.Field()
    product_desc = scrapy.Field()
    product_image = scrapy.Field()
    product_see_more = scrapy.Field()