import scrapy


class LagouproSpider(scrapy.Spider):
    name = 'lagoupro'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://www.lagou.com/']

    def parse(self, response):
        pass
