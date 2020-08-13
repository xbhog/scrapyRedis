# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RecruitmentnetworkItem(scrapy.Item):
    title = scrapy.Field()
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    site = scrapy.Field()
