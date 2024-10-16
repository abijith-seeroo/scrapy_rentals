import scrapy

class AperturentSpider(scrapy.Spider):
    name = "aperturent"
    allowed_domains = ["aperturent.com"]
    location_code = "DC"  # You can change this to 'DC', 'ATL', 'DAL', etc.

    def start_requests(self):
        # 1. Send a request to set the location
        location_url = f"https://aperturent.com/set-location/{self.location_code}"
        yield scrapy.Request(
            url=location_url,
            callback=self.after_location_set
        )

    def after_location_set(self, response):
        # 2. Now that the location is set, request the product page
        product_url = "https://aperturent.com/lenses/Canon-EF"
        yield scrapy.Request(url=product_url, callback=self.parse_products)

    def parse_products(self, response):
        # 3. Extract product details and pricing
        for product in response.css('div.product-listing'):
            product_name = product.css('div.product-listing-title a::text').get()
            product_url = response.urljoin(product.css('div.product-listing-title a::attr(href)').get())
            product_image = product.css('div.product-listing-img-container img::attr(data-src)').get()

            # Extract available rental periods and prices
            rental_periods = []
            for option in product.css('select[name="PRODUCT_OPTIONS"] option'):
                period = option.css('::text').get()
                if period and 'select rental period' not in period.lower():
                    rental_periods.append(period.strip())

            yield {
                'title': product_name,
                'product_link': product_url,
                'image_url': product_image,
                'price': rental_periods,
                'product_location': self.location_code,
            }
