import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


# Using google sheet as database
class CalendarSpider(CrawlSpider):
    name = "calendar"
    allowed_domains = ["nftcalendar.io"]
    start_urls = ["https://nftcalendar.io"]

    rules = (
        Rule(
            LinkExtractor(
                restrict_xpaths=r"//article//div[@class='tribe-events-calendar-list__event-featured-image-wrapper tribe-common-g-col']/a"
            ),
            callback="parse_item",
            follow=True,
        ),
        Rule(
            LinkExtractor(
                restrict_xpaths=r"//li[@class='tribe-events-c-nav__list-item tribe-events-c-nav__list-item--next']/a",
            ),
        ),
    )

    def parse_item(self, response):
        yield {
            "title": response.xpath(
                "//h1[@class='tribe-events-single-event-title']/text()"
            ).get(),
            "start_date": response.xpath(
                "//div[@class='tribe-events-schedule tribe-clearfix']/h2/span[1]/text()"
            ).get(),
            "end_date": response.xpath(
                "//div[@class='tribe-events-schedule tribe-clearfix']/h2/span[2]/text()"
            ).get(),
            "description": str(
                response.xpath(
                    "//div[@class='tribe-events-single-event-description tribe-events-content']/p/text()"
                ).getall()
            ),
            "event_category": str(
                response.xpath(
                    "//dd[@class='tribe-events-event-categories']/a/text()"
                ).getall()
            ),
            "event_tags": str(
                response.xpath("//dd[@class='tribe-event-tags']/a/text()").getall()
            ),
            "website": str(
                response.xpath(
                    "//dd[@class='tribe-events-event-url']/a/text()"
                ).getall()
            ),
            "venue": str(
                response.xpath("//dd[@class='tribe-venue']/a/text()").getall()
            ),
            "other_header": str(
                response.xpath(
                    "//div[@class='tribe-events-meta-group tribe-events-meta-group-other']/dl/dt/text()"
                ).getall()
            ),
            "others": str(
                response.xpath(
                    "//div[@class='tribe-events-meta-group tribe-events-meta-group-other']/dl/dd/text()"
                ).getall()
            ),
            "creator_header": str(
                response.xpath(
                    "//div[@class='tribe-events-meta-group tribe-events-meta-group-organizer']/dl/dt/text()"
                ).getall()
            ),
            "creator": str(
                response.xpath(
                    "//div[@class='tribe-events-meta-group tribe-events-meta-group-organizer']/dl/dd/text()"
                ).getall()
            ),
        }
