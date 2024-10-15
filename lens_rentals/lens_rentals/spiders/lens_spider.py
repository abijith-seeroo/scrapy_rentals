import scrapy
import random
import asyncio
from scrapy_playwright.page import PageMethod

class LensSpider(scrapy.Spider):
    name = 'lens_spider'
    page_number = 1  # Start at page 1
    max_pages = 330  # Max number of pages to scrape

    def start_requests(self):
        """Initialize the first request using Playwright."""
        yield self.make_request(self.page_number)

    def make_request(self, page):
        """Construct and return a new Scrapy request."""
        url = self.construct_url(page)
        self.logger.info(f"Scraping page {page}: {url}")

        return scrapy.Request(
            url=url,
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    PageMethod("wait_for_selector", "div.product-table"),
                    PageMethod("wait_for_timeout", random.randint(2000, 5000)),  # Random wait
                ]
            ),
            callback=self.parse,
            errback=self.handle_failure,
            dont_filter=True
        )

    def construct_url(self, page):
        """Construct the pagination URL based on the page number."""
        return (
            f"https://www.lensrentals.com/catalog_search?page={page}"
            "&sort_by=heat&filters={%22string_filters%22:[],%22number_filters%22:[],"
            "%22number_range_filters%22:[]}&q="
        )

    async def parse(self, response):
        """Parse the product data from the response."""
        products = response.css("div.product-item")

        # Handle pages with no products
        if not products:
            self.logger.warning(f"No products found on page {self.page_number}.")
            self.save_html(response)
            return

        # Extract product data
        for product in products:
            yield {
                'title': product.css('div.name::text').get().strip(),
                'image_url': product.css('div.product-img img::attr(src)').get(),
                'price': product.css('div.pricing ::text').get().strip(),
                'product_link': product.css('a::attr(href)').get(),
            }

        # Move to the next page
        self.page_number += 1
        if self.page_number <= self.max_pages:
            if self.page_number % 10 == 0:  # Restart context every 10 pages
                self.logger.info(f"Restarting Playwright browser context at page {self.page_number}")
                await response.meta['playwright_page'].context.close()
                await asyncio.sleep(2)  # Give the browser time to restart

            # Continue scraping the next page
            yield self.make_request(self.page_number)

    def save_html(self, response):
        """Save the HTML of the response for debugging."""
        filename = f"page_{self.page_number}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(response.text)
        self.logger.info(f"Saved HTML of page {self.page_number} to {filename}")

    def handle_failure(self, failure):
        """Handle any request failures."""
        self.logger.error(f"Request failed: {failure.request.url}")
