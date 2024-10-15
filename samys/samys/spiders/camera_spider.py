from xml.sax import parse

import scrapy
from ..items import WebscrapyCamera



class CameraSpider(scrapy.Spider):
    name = 'camera_spider'
    start_urls = ['https://www.samys.com/c/Photography/1/846.html?start=0']

    def parse(self, response):
        items=WebscrapyCamera()
        all_div_quote= response.css('div.floatContainer.product-list-row')
        for quote in all_div_quote:
            title=quote.css('div[itemprop="name"] h2::text').get()
            image_url=quote.css('div.product-image-container img::attr(src)').get()
            image_url = response.urljoin(image_url)
            price=quote.css('div.rental-price-column .price-amount::text').get()
            product_link=quote.css('div[itemprop="name"] a::attr(href)').get()
            product_link = response.urljoin(product_link)
            items['title']=title
            items['image_url']=image_url
            items['price']=price
            items['product_link']=product_link
            items['product_location']=""

            yield items

        next_page = response.css('li.pagination-next-container a::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)  # Ensure absolute URL
            self.logger.info(f"Following next page: {next_page_url}")
            yield scrapy.Request(next_page_url, callback=self.parse)