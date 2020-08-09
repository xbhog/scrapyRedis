# -*- coding: utf-8 -*-
#该spider为Scrapy的基础代码
import scrapy
from JDscrapy.JDspider import JdspiderItem
import json

class JdproSpider(scrapy.Spider):
    name = 'JDpro'
    start_urls = ['https://book.jd.com/booksort.html']

    def parse(self, response):
        #获取图书大分类中的列表
        big_node_list = response.xpath("//div[@class='mc']//dt/a")

        # 【：1】切片，先获取一类数据测试
        for big_node in big_node_list[:1]:
            #大分类的名称
            big_category = big_node.xpath("./text()").extract_first()
            #大分类的URL
            big_category_link = response.urljoin(big_node.xpath("./@href").extract_first())
            # print(big_category, big_category_link)
            # 获取所有图书小分类节点列表
            #注意点---获取兄弟节点的xpath语法结构；小分类的整体节点
            small_node_list = big_node.xpath("../following-sibling::dd[1]/em/a")
            #【：1】切片，先获取一类数据测试
            for small_node in small_node_list[:1]:
                temp = {}
                temp['big_category'] = big_category
                temp['big_category_link'] = big_category_link
                #获取小分类的名称
                temp['small_category'] = small_node.xpath("./text()").extract_first()
                #获取小分类的URL
                temp['small_category_link'] = response.urljoin(small_node.xpath("./@href").extract_first())
                # print(temp)
                #注意点，筛选出来的数据持续传输，meta的使用
                yield scrapy.Request(
                    url=temp['small_category_link'],
                    callback= self.parse_book_link,
                    #上面保存的item传递给下一个解析函数
                    meta = {'data':temp}
                )

    #解析详情
    def parse_book_link(self,response):
        temp = response.meta['data']

        #获取到Book的标签
        book_list = response.xpath("//*[@id='J_goodsList']/ul/li/div")
        # print(len(book_list))
        #遍历标签页
        for book in book_list:
            item = JdspiderItem()

            item['big_category'] = temp['big_category']
            item['big_category_link'] = temp['big_category_link']
            item['small_category'] = temp['small_category']
            item['small_category_link'] = temp['small_category_link']
            #书的名字
            item['bookname'] = book.xpath('./div[3]/a/em/text()|./div/div[2]/div[2]/div[3]/a/em/text()').extract_first()
            #书的作者
            item['author'] = book.xpath('./div[4]/span[1]/a/text()|./div/div[2]/div[2]/div[4]/span[1]/span[1]/a/text()').extract_first()
            #书的URL
            item['link'] = response.urljoin(book.xpath('./div[1]/a/@href|./div/div[2]/div[2]/div[1]/a/@href').extract_first())
            # print(item)
            # 获取图书编号，目的拼接图书的Price
            skuid = book.xpath('.//@data-sku').extract_first()
            # skuid = book.xpath('./@data-sku').extract_first()
            # print("skuid:",skuid)
            # 拼接图书价格地址
            pri_url = 'https://p.3.cn/prices/mgets?skuIds=J_' + skuid
            # print(pri_url)

            yield scrapy.Request(url=pri_url, callback=self.parse_price, meta={'meta_1': item})
            #拿到一条数据测试，可以开启
            break
    def parse_price(self,response):
        #拿到传递过来的item
        item = response.meta['meta_1']
        #解析json页面
        dict_data = json.loads(response.body)
        #解析价钱，传递到item中
        item['price'] = dict_data[0]['p']
        # print(item)
        yield item
