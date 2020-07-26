import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from sunsite.items import SunsiteItem
from scrapy_redis.spiders import RedisCrawlSpider

class SunprocrawlSpider(RedisCrawlSpider):
    name = 'Sunprocrawl'
    # allowed_domains = ['www.xxx.com']
    # start_urls = ['http://wz.sun0769.com/political/index/politicsNewest?id=1&page=1']
    redis_key = 'sunurl'
    rules = (
        Rule(LinkExtractor(allow=r'id=1&page=\d+'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        li_list = response.xpath("/html/body/div[2]/div[3]/ul[2]//li")
        for li in li_list:
            item = SunsiteItem()
            item['title'] = li.xpath("./span[3]/a/text()").extract_first()
            status = li.xpath("./span[2]/text()").extract_first().split('\n                        ')[1]

            item['status'] = status.split("\n                    ")[0]
            # print(item)
            yield item