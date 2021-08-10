import scrapy


class GeekvapeSpider(scrapy.Spider):
    name = "geekvape"
    allowed_domains = ["www.cigabuy.com"]

    def start_request(self):
        yield scrapy.Request(
            url="https://www.cigabuy.com/geekvape-c-99_140.html",
            callback=self.parse,
            headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
            },
        )

    def parse(self, response):
        for product in response.xpath("//div[@class='p_box_wrapper']"):
            yield {
                "title": product.xpath(".//a[@class='p_box_title']/text()").get(),
                "url": response.urljoin(
                    product.xpath(".//a[@class='p_box_title']/@href").get()
                ),
                "rating": product.xpath(".//div[@class='p_box_star']/a/text()").get(),
                "discounted_price": product.xpath(
                    ".//div[@class='p_box_price cf']/span[1]/text()"
                ).get()
                or product.xpath(".//div[@class='p_box_price cf']/text()").get(),
                "original_price": product.xpath(
                    ".//div[@class='p_box_price cf']/span[2]/text()"
                ).get(),
            }

        next_page = response.xpath(
            "//div[@id='pageDiv1']/a[@class='nextPage']/@href"
        ).get()

        if next_page:
            yield scrapy.Request(
                url=next_page,
                callback=self.parse,
                headers={
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
                },
            )
