import scrapy
from selenium import webdriver
import time
# 导入 ActionChains 类,鼠标链
from selenium.webdriver import ActionChains
from pypinyin import lazy_pinyin
from lxml import etree

from RecruitmentNetwork.items import RecruitmentnetworkItem


class LagouproSpider(scrapy.Spider):
    name = 'lagoupro'
    # allowed_domains = ['www.xxx.com']

    def __init__(self,site):
        super(LagouproSpider, self).__init__()
        # 中文转拼音
        pinyin = lazy_pinyin(site)
        # print(pinyin)
        self.site = pinyin[0] + pinyin[1]
        # print(self.site)
        # 字符串拼接---得到地域URL
        self.start_urls = [f"https://www.lagou.com/{self.site}-zhaopin/"]

    #获取第一页链接和内容并实现翻页
    def parse(self, response):
        driver = webdriver.Chrome()
        driver.get(response.url)
        # 找到文本框输入内容
        driver.find_element_by_id("keyword").send_keys("python")
        # 搜索
        search_button = driver.find_element_by_id("submit")
        time.sleep(1)
        ActionChains(driver).move_to_element(search_button).click(search_button).perform()
        time.sleep(1)
        #去掉给也不要
        driver.find_element_by_class_name("body-btn").click()

        # 解析selenium发过来的response数据
        str_html = driver.page_source
        html = etree.HTML(str_html)
        try:
            # 父标签---所需要信息标签上的父标签
            div_list = html.xpath("//ul[@class='item_con_list']/li")
            item = RecruitmentnetworkItem()
            for div in div_list:
                item['title'] = div.xpath(".//h3/text()")[0]
                # 判断title是否为空
                if item['title'] == None:
                    continue
                item['company_name'] = div.xpath(".//div[@class='company_name']/a/text()")[0]
                item['company_url'] = div.xpath(".//div[@class='company_name']/a/@href")[0]
                item['site'] = div.xpath(".//span[@class='add']/em//text()")[0]
                # yield item
                print(item)

        except:
            print('没有数据')

        time.sleep(5)
        driver.quit()

