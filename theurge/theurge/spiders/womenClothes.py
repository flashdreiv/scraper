import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
from selenium.webdriver.chrome.options import Options


class WomenClothesSpider(scrapy.Spider):
    name = "womenClothes"
    allowed_domains = ["www.theurge.com"]

    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.theurge.com/women/search/?retailers=Tuchuzy",
            wait_time=3,
            callback=self.parse,
        )

    def parse(self, response):
        driver = response.meta["driver"]

        html = driver.page_source
        response_obj = Selector(text=html)

        products = response_obj.xpath("//article[@class='_2Mqpk']")

        for product in products:
            yield {
                "image_url": product.xpath(".//img[@class='_58p9P']/@srcset").get(),
                "product_name": product.xpath(".//p[@class='_3I42k']/text()").get(),
                "price": product.xpath(".//div[@class='eP0wn _2xJnS']/text()[2]").get(),
            }
