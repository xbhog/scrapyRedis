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
import sys,os
sys.path.append('..')
path = os.getcwd()+'/bin/driver/chromedriver.exe'
print(path)
class SeleniumDownloaderMiddleware:
    def process_request(self,request,spider):
        driver = webdriver.Chrome(executable_path=path)
        driver.get(request.url)
        time.sleep(5)
        driver.quit()