#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import re
from chrome_driver import ChromeDriver
from sms_platform_api import Ailezan
from multiprocessing import Pool

'2017年7月13日17:39:06:重构Onedrive'


class settings():
    reg_url = 'https://onedrive.live.com/?invref=f1362f90ffdfb4a9&invscr=90'
    times = 1
    pid = '5062'
    account_psw = 'Q209209209x'
    account_email = ''


class OnedriveProj():

    def __init__(self):
        self.setting = settings()

        # 申请手机号码
        self.get_phonenumber()
        # todo 如果这里没获取到咋整？
        # 打开浏览器请求验证码

        self.send_verificationcode()
        self.sms_platform.add_ignore_list(self.setting.pid,self.phonenumber)
        #
        # # 获取手机上的验证码，注册
        # self.register()
        # result=self.check_result()

        pass

    def get_phonenumber(self):
        self.sms_platform = Ailezan()
        self.phonenumber = self.sms_platform.get_mobilenumber(self.setting.pid)

    def send_verificationcode(self):
        self.c = ChromeDriver(reg_url=self.setting.reg_url)
        self.c.send_verifycode(self.phonenumber, psw=self.setting.account_psw)
        pass

    def register(self):
        # 收验证码
        verifycode_raw = self.sms_platform.receive_verificationcode()
        verifycode = re.search(r'(?<=\?)\d{4}(?=\?)', verifycode_raw).group()

        # 提交验证码注册

        pass

    def check_result(self):
        pass


if __name__ == '__main__':
    import time
    p = Pool(1)

    for i in range(10):
        time.sleep(2)
        p.apply_async(OnedriveProj, args=())#多进程运行函数
    print('waiting for all process done...')
    p.close()
    p.join()
