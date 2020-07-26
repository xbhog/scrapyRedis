import scrapy


class SunsiteItem(scrapy.Item):
    title = scrapy.Field()
    status = scrapy.Field()