from xml.sax import parse

import scrapy
from ..items import Webscrapycam



class CameraSpider(scrapy.Spider):
    name = 'cam_spider'
    start_urls = ['https://www.lensprotogo.com/rent/category/cameras/?page=1&querystring_key=page']

    def parse(self, response):
        items=Webscrapycam()
        all_divs = response.css('div.gear-item')

        # Stop the spider if no products are found
        if not all_divs:
            self.logger.info("No products found on this page. Stopping the spider.")
            return  # Stop the function and spider

        # Loop through all product divs
        for div in all_divs:
            # Extract product details
            title = div.css('p.item-description a::text').get()
            image_url = div.css('a.image_link img::attr(src)').get()
            price = div.css('p.item-price a::text').get()
            product_link = div.css('p.item-description a::attr(href)').get()


            # Store product details in the item
            items['title'] = title
            items['image_url'] = image_url
            items['price'] = price
            items['product_link'] = response.urljoin(product_link)
            items['product_location'] = ""  # Not available in this structure

            yield items
        # page=response.css('endless_container @href')
        # next_page = 'https://www.lensprotogo.com'+str(page)
        # yield response.follow(next_page, callback=self.parse)

        next_page = response.css('div.endless_container a.endless_more::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            self.logger.info(f"Following next page: {next_page_url}")
            yield response.follow(next_page_url, callback=self.parse)