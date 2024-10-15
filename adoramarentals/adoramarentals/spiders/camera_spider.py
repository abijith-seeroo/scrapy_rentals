import scrapy
from ..items import AdoramarentalsItem

class CameraSpider(scrapy.Spider):
    name = 'camera_spider'
    start_urls = ['https://www.adoramarentals.com/l/Cameras?startAt=0']

    # Custom headers to mimic a browser
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
        'ROBOTSTXT_OBEY': False,  # Ignore robots.txt rules
        'COOKIES_ENABLED': True,  # Enable cookies if required
    }

    def parse(self, response):
        all_products = response.css('div.item')
        for product in all_products:
            product_name = product.css('div.item-details h2 a::text').get().strip()
            product_image = product.css('div.item-img a img::attr(src)').get()
            product_price = product.css('strong.your-price::text').get().strip()
            product_link = product.css('div.item-details h2 a::attr(href)').get()

            # Join URLs properly
            if product_image:
                product_image = response.urljoin(product_image)
            if product_link:
                product_link = response.urljoin(product_link)

            camera = AdoramarentalsItem()
            camera['title'] = product_name
            camera['image_url'] = product_image
            camera['price'] = product_price
            camera['product_link'] = product_link
            camera['product_location'] = ""

            yield camera

        next_page = response.css('a.page-next::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)
