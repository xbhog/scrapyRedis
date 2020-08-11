import scrapy
from selenium import webdriver
import time
# 导入 ActionChains 类,鼠标链
from selenium.webdriver import ActionChains
from pypinyin import lazy_pinyin
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


        #点击下一页
        # driver.find_element_by_class_name("pager_next ").click()
        time.sleep(5)
        driver.quit()


