import scrapy
from scrapy_selenium import SeleniumRequest


class ExampleSpider(scrapy.Spider):
    name = "example"

    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.duckduckgo.com",
            wait_time=3,
            screenshot=True,
            callback=self.parse,
        )

    def parse(self, response):
        driver = response.meta["driver"]
        search_input = driver.find_element_
