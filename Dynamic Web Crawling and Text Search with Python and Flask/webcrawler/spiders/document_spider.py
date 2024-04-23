import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os

class DocumentSpider(scrapy.Spider):
    name = 'document_spider'

    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 5,
        'AUTOTHROTTLE_MAX_DELAY': 60,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0,
        'DEPTH_LIMIT': 3  # Maximum depth of crawling
    }

    def __init__(self, seed_url='http://books.toscrape.com', max_pages=100, *args, **kwargs):
        super(DocumentSpider, self).__init__(*args, **kwargs)
        self.start_urls = [seed_url]  # Seed URL
        self.max_pages = max_pages    # Maximum number of pages to crawl
        self.count = 0                # Counter to track number of pages crawled

    def parse(self, response):
        if self.count < self.max_pages:
            self.count += 1
            # Extract a filename from the URL or generate a default one if not possible
            page = response.url.split("/")[-1] or 'index'
            filename = f'documents/{page}.html'

            # Ensure the 'documents' directory exists
            os.makedirs('documents', exist_ok=True)

            with open(filename, 'wb') as f:
                f.write(response.body)
            self.log(f'Saved file {filename}')

            # Follow links on the page
            for a in response.css('a::attr(href)'):
                yield response.follow(a, callback=self.parse)
