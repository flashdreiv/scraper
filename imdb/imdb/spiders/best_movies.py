import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = "best_movies"
    allowed_domains = ["imdb.com"]

    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.imdb.com/chart/top/?ref_=nv_mv_250",
            headers={"User-Agent": self.user_agent},
        )

    rules = (
        Rule(
            LinkExtractor(restrict_xpaths="//td[@class='titleColumn']/a"),
            callback="parse_item",
            follow=True,
            process_request="set_user_agent",
        ),
    )

    def set_user_agent(self, request, response):
        request.headers["User-Agent"] = self.user_agent
        return request

    def parse_item(self, response):
        yield {
            "title": response.xpath(
                "//div[@class='TitleBlock__TitleContainer-sc-1nlhx7j-1 jxsVNt']/h1/text()"
            ).get(),
            "year": response.xpath(
                "//li[@class='ipc-inline-list__item']/a/text()"
            ).get(),
            "rating": response.xpath(
                "//span[@class='AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV']/text()"
            ).get(),
            "duration": response.xpath("//li[@role='presentation'][3]/text()").get(),
            "movie_url": response.url,
        }
