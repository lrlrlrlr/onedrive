#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import re
from chrome_driver import ChromeDriver
from chrome_driver import randomname
from sms_platform_api import Ailezan
from multiprocessing import Pool
import time

'2017年7月13日17:39:06:重构Onedrive'
'2017年7月26日00:43:09:重构了大部分,能跑通,可能异常处理方面还不是很完善, '
#todo 注册完之后的登录还没做
#todo 多线程注册的实现
#todo phamtomJS的实现
#todo 登录速度慢的问题还要解决



class settings():
    reg_url = 'https://onedrive.live.com/?invref=f1fabd49bc823320&invscr=90'
    times = 2
    pid = '5062'
    account_psw = 'Q209209209x'
    account_email = randomname(13)



class OnedriveProj():


    def __init__(self):
        #初始化各种flag和setting
        self.flag_getphone=None
        self.flag_sendvcode=None
        self.flag_recv_vcode=None
        self.flag_reg=None
        self.setting = settings()
        self.sms_platform=Ailezan()

        #开始执行
        times=0
        while times < self.setting.times:
            self.c=ChromeDriver()#todo 这里我没办法登出, 所以只能重开driver
            print('当前成功次数:%s'%times)
            # 申请手机号码
            self.get_phonenumber()

            # 打开浏览器请求验证码
            if self.flag_getphone is True:

                self.send_vcode()

                if self.flag_sendvcode is True:
                    #查收验证码
                    self.recv_vcode()

                    if self.flag_recv_vcode is True:

                        self.register()

                        if self.flag_reg is True:
                            self.check_result()
                            times+=1


        pass

    def get_phonenumber(self):

        self.phonenumber = self.sms_platform.get_mobilenumber(self.setting.pid)
        self.flag_getphone=True

    def send_vcode(self):

        self.c.send_vcode(self.setting.reg_url,self.phonenumber,psw=self.setting.account_psw)
        self.flag_sendvcode=True

    def recv_vcode(self):
        print('尝试接受验证码..')
        # 收验证码
        attempt_times=0
        while attempt_times<10:
            try:
                verifycode_raw = self.sms_platform.receive_verificationcode(pid=self.setting.pid,mobile=self.phonenumber)
                assert verifycode_raw is not None
            except:
                print('尚未收到验证码..',attempt_times)
                attempt_times+=1
                time.sleep(3)
            else:
                self.verifycode = re.search(r'(?<=\?)\d{4}(?=\?)', verifycode_raw).group()
                self.sms_platform.add_ignore_list(pid=self.setting.pid,mobile=self.phonenumber)
                self.flag_recv_vcode=True
                break
        else:
            print ('接受短信超时!')
            self.sms_platform.add_ignore_list(pid=self.setting.pid,mobile=self.phonenumber)


    def register(self):
        # 提交验证码注册
        self.c.input_vcode(self.verifycode)
        #填写新邮箱并确认注册
        attempt_times=0
        while self.c.c.title != '添加电子邮件':
            time.sleep(1)
            attempt_times+=1
            time.sleep(3)
            if attempt_times>20:
                raise '注册邮箱页面跳转找不到入口'
        else:
            self.setting.account_email=self.c.input_mail(self.setting.account_email)
            self.flag_reg=True



    def check_result(self):
        print('注册时间:{}\n注册手机号:{}\n注册密码:{}\n注册邮箱:{}'.format(time.ctime(),self.phonenumber,self.setting.account_psw,self.setting.account_email))
        pass


if __name__ == '__main__':
    t=OnedriveProj()