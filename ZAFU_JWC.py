#! python3
# coding:utf-8
"""
ZAFU_JWC Spider ver.0.16.6
Author: 0xLLLLH
Description: This spider is designed to login into ZAFU's JWC system
"""
import re
import random
import time
from urllib import request, parse, error
from http import cookiejar
__author__ = '0xLLLLH'


class JWC:
    def __init__(self):
        # urls should end with '/'
        self.urls = ['http://210.33.60.2/', 'http://210.33.60.8/', 'http://210.33.60.6/']
        self.proxyUrls = ['201.219.174.77:8080/']
        self.postData = {
            'txtUserName': '201305070126',
            'TextBox2': '123456',
            'txtSecretCode': '',
            'RadioButtonList1': '学生',
            'Button1': '',
            'lbLanguage': '',
            'hidPdrs': '',
            'hidsc': ''
        }
        self.captcha = ""
        # self.post = parse.urlencode(self.postData).encode('gbk')
        self.proxyHandler = request.ProxyHandler({'http': self.proxyUrls[0]})   # TODO: Add code to auto select proxy
        self.cookieHandler = request.HTTPCookieProcessor(cookiejar=cookiejar.CookieJar())
        self.opener = request.build_opener(self.cookieHandler, request.HTTPHandler)
        # self.opener.addheaders = list(map(lambda a, b: (a, b), self.headers_login.keys(), self.headers_login.values()))
        request.install_opener(self.opener)

    def get_captcha(self, url):
        # Url here is the url of captcha
        # When getting a captcha, cookie would be saved.
        # return value indicates if get captcha success
        try:
            response = self.opener.open(url)
            img = response.read()
        except error.HTTPError as e:
            print("{0}:{1}".format(e.code, e.reason))
        else:
            try:
                out = open('captcha.gif', 'wb')
                out.write(img)
                out.flush()
                out.close()
                print('get captcha success')
            except IOError as e:
                print('get captcha error {0}:{1}'.format(e.code, e.reason))
                return False
        captcha = input("Please open captcha.gif and type captcha :")
        self.captcha = captcha
        return True

    def get_form(self, url):
        # self.headers_form['Referer'] = 'http://jwc.zafu.edu.cn/'
        try:
            req = request.Request(url=url + 'default2.aspx')
            response = request.urlopen(req)
            content = response.read().decode('gbk')
            view_state = re.compile('name="__VIEWSTATE".*?value="(.*?)"').findall(content)
            if view_state:
                self.postData['__VIEWSTATE'] = view_state[0]
            view_state_generator = re.compile('name="__VIEWSTATEGENERATOR".*?value="(.*?)"').findall(content)
            if view_state_generator:
                self.postData['__VIEWSTATEGENERATOR'] = view_state_generator[0]
            self.get_captcha(url+'CheckCode.aspx')
        except error.HTTPError as e:
            print('get form error {0}:{1}'.format(e.code, e.reason))
        else:
            if response:
                response.close()

    def login(self, url):
        url += 'default2.aspx'
        try:
            # TODO: Add code to auto select url
            self.postData['txtSecretCode'] = self.captcha
            req = request.Request(url, data=parse.urlencode(self.postData).encode('gbk'))
            response = self.opener.open(req)
            content = response.read().decode('gbk')
            print(response.info())
            print(content)
        except error.HTTPError as e:
            print('login error {0}:{1}'.format(e.code, e.reason))
            return False
        else:
            if response:
                response.close()
                return True

    def start(self):
        while True:
            idx = int(random.random() * len(self.urls))
            print('Select url:'+self.urls[idx])
            self.get_form(self.urls[idx])
            if not self.login(self.urls[idx]):
                print("Login fail , retry in 5 seconds...")
                time.sleep(5)
            else:
                print("login success")
                break


if __name__ == "__main__":
    spider = JWC()
    spider.start()
