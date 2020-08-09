import scrapy



class LagouproSpider(scrapy.Spider):
    name = 'lagoupro'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://www.lagou.com/']
    #获取第一页链接和内容并实现翻页
    def parse(self, response):
        print(response.text)
