# class RecruitmentnetworkDownloaderMiddleware:
#
#     def process_request(self, request, spider):
#
#         return None
#
#     def process_response(self, request, response, spider):
#
#         return response
#
#     def process_exception(self, request, exception, spider):
#
#         pass
#
#     def spider_opened(self, spider):
#         spider.logger.info('Spider opened: %s' % spider.name)
from selenium import webdriver
import time
# 导入 ActionChains 类,鼠标链
from selenium.webdriver import ActionChains
from scrapy.http import HtmlResponse


class SeleniumDownloaderMiddleware:
    def process_request(self, request, spider):
        # driver = webdriver.Chrome()
        #避过网站对selenium的检测
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(options=options)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
               Object.defineProperty(navigator, 'webdriver', {
                 get: () => undefined
              })
            """})

        driver.get(request.url)
        time.sleep(2)
        # 取消拉钩出现的切换城市
        click = driver.find_element_by_id("cboxClose")
        ActionChains(driver).move_to_element(click).click(click).perform()
        time.sleep(1)
        # 找到文本框输入内容
        search_input = driver.find_element_by_id("search_input").send_keys("python")
        # 搜索
        search_button = driver.find_element_by_id("search_button")
        time.sleep(1)
        ActionChains(driver).move_to_element(search_button).click(search_button).perform()
        time.sleep(1)
        body_btn = driver.find_element_by_class_name("body-btn").click()
        # 以上方式解决拉钩网站出现的弹窗问题，纯selenium
        # 下面获取网页源码退出selenium并且返回response到lagoupro
        html = driver.page_source
        time.sleep(5)
        driver.quit()
        return HtmlResponse(url=request.url,body=html,request=request,encoding="utf-8")
