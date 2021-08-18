# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter


import gspread


class NftcalendarPipeline:
    def open_spider(self, spider):
        gc = gspread.service_account(
            filename="/home/drei/Desktop/scraper/nftcalendar/nftcalendar/creds.json"
        )
        self.sh = gc.open("scraper_sample").sheet1
        return self.sh

    def process_item(self, item, spider):
        self.sh.append_row(
            [
                item["title"],
                item["start_date"],
                item["end_date"],
                item["event_category"],
                item["event_tags"],
                item["website"],
                item["venue"],
                item["other_header"],
                item["others"],
                item["creator_header"],
                item["creator"],
                item["description"],
            ]
        )
        return item
