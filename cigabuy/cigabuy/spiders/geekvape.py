import scrapy


class GeekvapeSpider(scrapy.Spider):
    name = "geekvape"
    allowed_domains = ["www.cigabuy.com"]
    start_urls = ["https://www.cigabuy.com/geekvape-c-99_140.html"]

    def parse(self, response):
        for product in response.xpath("//div[@class='p_box_wrapper']"):
            yield {
                "title": product.xpath(".//a[@class='p_box_title']/text()").get(),
                "rating": product.xpath(".//div[@class='p_box_star']/a/text()")
                .get()
                .replace("()", ""),
                "price": product.xpath(
                    ".//div[@class='p_box_price cf']/span[1]/text()"
                ).get(),
            }
