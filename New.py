#!/usr/bin/env python3
#-*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

'2017年7月13日17:39:06:重构Onedrive'


def main(url,times):
	# _succ_times=0
	# while _succ_times<times:
	# 	#打开浏览器,并申请手机号码
	# 	phonenumber=Initialize()
	# 	SendVerifycode(phonenumber)
	#
	# 	Verifycode=ReceiveVerifycode()
	# 	Register(Verifycode)
	#
	# 	result=CheckResult()
	# 	if result is True:
	# 		_succ_times+=1

	# 	pass
	# else:
	pass


def Initialize(proxy_switch=True):
	global c
	if proxy_switch==True:#是否打开proxy
		proxy='127.0.0.1:1080'
		chrome_options=webdriver.ChromeOptions()
		chrome_options.add_argument('--proxy-server={}'.format(proxy))
	else:
		chrome_options=None

	c=webdriver.Chrome(executable_path=r'D:\DDL DATA\OneDrive\tools\chromedriver.exe',
	                   chrome_options=chrome_options)

	#下面这部分是测试
	url='https://onedrive.live.com/?invref=46101731aebb9508&invscr=90'
	c.get(url)
	element=WebDriverWait(c,10).until(EC.presence_of_element_located((By.XPath,'//*[@id="signup"]')))

	#todo 模块化短信API
	#登录API,查余额,token

	pass


def SendVerifycode():
	c.get()

	pass


def Register():
	pass


def CheckResult():
	pass
