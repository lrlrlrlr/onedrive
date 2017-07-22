from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random,time



class ChromeDriver():
    """控制chromedriver完成onedrive注册"""
    def __init__(self, reg_url='https://onedrive.live.com/?invref=f1362f90ffdfb4a9&invscr=90',driver_path=r'D:\DDL DATA\OneDrive\tools\chromedriver.exe', proxy_switch=True):
        if proxy_switch is True:  # 是否打开proxy
            proxy = '127.0.0.1:1080'
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--proxy-server={}'.format(proxy))
        else:
            chrome_options = None

        self.c = webdriver.Chrome(executable_path=r'D:\DDL DATA\OneDrive\tools\chromedriver.exe',
                                  chrome_options=chrome_options)
        self.reg_url = reg_url

    def test(self):
        self.c.get('https://www.baidu.com')


    def getelement(self,xpath):
        element = WebDriverWait(self.c, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath)))
        return element

    def send_verifycode(self, phonenumber, psw):

        # 打开邀请链接
        self.c.get(self.reg_url)

        # 点击注册帐号
        self.getelement('//*[@id="signup"]').click()
        self.getelement('//*[@id="phoneSwitch"]').click()

        # 填入账号密码
        self.getelement('//*[@id="MemberName"]').send_keys(str(phonenumber))
        self.getelement('//*[@id="Password"]').send_keys(str(psw))
        self.getelement('//*[@id="iSignupAction"]').click()
        print('发送验证码成功:{}'.format(phonenumber))


