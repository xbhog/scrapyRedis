import scrapy
from sunsite.items import SunsiteItem

class SunproSpider(scrapy.Spider):
    name = 'sunpro'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['http://wz.sun0769.com/political/index/politicsNewest?id=1&page=1']

    def parse(self, response):
        li_list = response.xpath("/html/body/div[2]/div[3]/ul[2]//li")
        for li in li_list:
            item = SunsiteItem()
            item['title'] = li.xpath("./span[3]/a/text()").extract_first()
            status= li.xpath("./span[2]/text()").extract_first().split('\n                        ')[1]

            item['status'] = status.split("\n                    ")[0]
            # print(item)
            yield item
