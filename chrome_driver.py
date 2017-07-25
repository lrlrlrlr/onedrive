from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import random,time

def randomname(k=8):
    return 'l'+''.join(random.choices('qwertyuiopasdfghjklzxcvbnmn1234567890',k=k))


class ChromeDriver():
    """控制chromedriver完成onedrive注册"""
    def __init__(self, driver_path=r'D:\DDL DATA\OneDrive\tools\chromedriver.exe', proxy_switch=True):
        if proxy_switch is True:  # 是否打开proxy
            proxy = '127.0.0.1:1080'
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--proxy-server={}'.format(proxy))
        else:
            chrome_options = None

        self.c = webdriver.Chrome(executable_path=r'D:\DDL DATA\OneDrive\tools\chromedriver.exe',
                                  chrome_options=chrome_options)
        self.c.implicitly_wait(3)


    def test(self):
        self.c.get('https://www.baidu.com')


    def getelement(self,xpath,timeout=30):
        element = WebDriverWait(self.c, timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath)))
        return element

    def send_vcode(self,reg_url,phonenumber,psw='Q209209209a'):
        self.reg_url=reg_url
        # 打开邀请链接
        self.c.get(self.reg_url)

        # 点击注册帐号
        assert '登录' in self.c.page_source
        self.getelement('//*[@id="signup"]').click()
        assert '创建帐户' in self.c.page_source
        self.getelement('//*[@id="phoneSwitch"]').click()

        # 填入账号密码
        self.getelement('//*[@id="MemberName"]').send_keys(str(phonenumber))
        self.getelement('//*[@id="Password"]').send_keys(str(psw))
        self.getelement('//*[@id="Password"]').send_keys(Keys.RETURN)

        #确认跳转成功了
        self.check_send_vcode=0
        while '输入代码' not in self.c.page_source:

            if '输入代码' in self.c.page_source:
                print('发送验证码成功:{}'.format(phonenumber))
                break
            elif self.check_send_vcode>10:
                raise '发送验证码失败!'
            else:
                time.sleep(1)
                self.check_send_vcode+=1


    def input_vcode(self,vcode):

        assert '输入代码' in self.c.page_source
        self.getelement('//*[@id="VerificationCode"]').send_keys(str(vcode))
        self.getelement('//*[@id="iSignupAction"]').click()
        pass

    def input_mail(self,mailaddr):
        #点注册

        #todo assert '或从我们这里获取新的 Outlook 电子邮件' in self.c.page_source
        self.getelement('//*[@id="outlookEasiSwitch"]').click()
        #输入邮件
        #todo  assert '或使用你现有的电子邮件' in self.c.page_source
        self.getelement('//*[@id="iAliasName"]').send_keys(mailaddr)
        self.getelement('//*[@id="iAliasName"]').send_keys(Keys.RETURN)

        #输入完之后尝试查找错误信息
        try:
            errorinfo=self.getelement('//*[@id="iEmailAddressError"]',timeout=5)
            while errorinfo.text is not '':
                mailaddr=randomname(k=12)
                print(errorinfo.text)
                self.getelement('//*[@id="iAliasName"]').clear()
                self.getelement('//*[@id="iAliasName"]').send_keys(mailaddr)
                self.getelement('//*[@id="iAliasName"]').send_keys(Keys.RETURN)
                errorinfo=self.getelement('//*[@id="iEmailAddressError"]',timeout=5)
        finally:
            return mailaddr



if __name__ == '__main__':
    c=ChromeDriver()
    c.send_vcode('17098990000')