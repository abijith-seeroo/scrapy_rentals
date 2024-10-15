from xml.sax import parse

import scrapy
from ..items import WebscrapyCamera



class CameraSpider(scrapy.Spider):
    name = 'camera_spider'
    start_urls = ['https://aperturent.com/cameras']

    def parse(self, response):
        camera=WebscrapyCamera()
        all_div_quote=response.css('div.product-listing')
        for product in all_div_quote:
            product_name=product.css('div.product-listing-title a::text').get()
            # product_price=product.css('div.product-listing-description::text').get()
            product_image=product.css('div.product-listing-img-container img::attr(data-src)').get()
            product_see_more = product.css('div.product-listing-more-link a::attr(href)').get()

            if product_see_more:
                product_see_more = 'https://aperturent.com' + product_see_more
            camera['title']=product_name
            camera['price']=""
            camera['image_url']=product_image
            camera['product_link']=product_see_more
            camera['product_location']=""

            yield camera


