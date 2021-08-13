import scrapy
import json


class ClothesapiSpider(scrapy.Spider):
    name = "clothesApi"
    allowed_domains = ["https://api.theurge.com/search-results?page=1"]
    start_urls = [
        "https://api.theurge.com/search-results?page=1&currency=USD&gender=female&retailers=Tuchuzy&language=en&country=us&client=theurge"
    ]

    def parse(self, response):
        resp = json.loads(response.body)

        products = resp.get("data")
        page_size = resp.get("meta")["meta"]["pageSize"]
        max_page = round(float(resp.get("meta")["meta"]["total"]) / page_size)

        for product in products:

            yield {
                "image_url": product["attributes"]["e_image_urls_og"],
                "product_name": product["attributes"]["product_name"],
                "price": product["attributes"]["converted_sale_price"],
            }

        for i in range(2, max_page):
            yield scrapy.Request(
                url=f"https://api.theurge.com/search-results?page={i}&currency=USD&gender=female&retailers=Tuchuzy&language=en&country=us&client=theurge",
                callback=self.parse,
            )
