import random

import selenium
from retrying import retry
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from 一些项目.API.Caoma import *
from 一些项目.API.Xunma import *
from 一些项目.API.爱乐赞 import *


def getelement(xpath):
    element=WebDriverWait(c,10).until(EC.presence_of_element_located((By.XPATH,xpath)))
    return element


def writelog(usrname,psw,path='D://hotmail.txt'):
    with open(path,'a') as log:
        log.write('{}|{}|{}'.format(time.strftime('%Y-%m-%d %H:%M'),usrname,psw)+'\n')
        log.close()
        print('存储注册账号!')


@retry
def Onedrive_signup_send(url,phonenumber='17098903020',psw='psw209209A'):
    try:
        # 打开邀请链接
        c.get(url)

        # 点击注册帐号
        getelement('//*[@id="signup"]').click()
        getelement('//*[@id="phoneSwitch"]').click()

        # 填入账号密码
        getelement('//*[@id="MemberName"]').send_keys(str(phonenumber))
        getelement('//*[@id="Password"]').send_keys(str(psw))
        getelement('//*[@id="iSignupAction"]').click()
        print('发送验证码成功:{}'.format(phonenumber))
    except:
        print('singup error')
        raise 'singnup error'


def Onedrive_signup_verify(VerificationCode,userName='lr'+''.join(random.choices('1234567890asdfghjklzxcvbnm',k=11))):
    # 输入验证码
    getelement('//*[@id="VerificationCode"]').send_keys(str(VerificationCode))
    getelement('//*[@id="iSignupAction"]').click()

    # 等待验证验证码后的跳转
    while c.title!='添加电子邮件':
        time.sleep(1)
    else:
        print('验证码正确')
        # 填入随机生成的邮箱地址并提交注册
        while c.title=='添加电子邮件':
            getelement('//*[@id="outlookEasiSwitch"]').click()
            getelement('//*[@id="iAliasName"]').send_keys(userName)
            time.sleep(1)

            try:
                c.find_element_by_xpath('//*[@id="iNext"]').click()
                c.find_element_by_xpath('//*[@id="iNext"]').click()
            except:
                pass
            # 判定是否注册成功,若不成功则返回上一步重新填写邮箱提交
            # 等待页面加载完成再退出!

            try:
                if c.title=='OneDrive' or c.title=='文件 - OneDrive':
                    count=0#最后这个页面有时候刷不出来,加个判定
                    while c.title!='文件 - OneDrive':
                        time.sleep(3)
                        count+=1
                        if count>10:
                            count=0
                            c.refresh()
                        #todo 这里容易死循环

                        try:
                            time.sleep(2)
                            c.get('https://onedrive.live.com/?v=managestorage')
                            print('校验结果,查询推荐人信息:',c.find_element_by_xpath(
                                '//*[@id="appRoot"]/div/div[2]/div[5]/div[1]/div/div/table[2]/tbody/tr[1]/td[1]/span['
                                '1]/span').text)
                        except:
                            print('校验结果的时候出错了!')
                        finally:
                            return True
                else:
                    print('用户名不对,重试..')
                    userName='lr'+''.join(random.choices('1234567890qwertyuiopasdfghjklzxcvbnm',k=11))

            except selenium.common.exceptions.TimeoutException:
                print('验证成功后打开超时!')
                pass


def main_Xunma():
    # 绑定chromedriver
    global c
    c=webdriver.Chrome(executable_path=r'D:\OneDrive\tools\chromedriver.exe')
    # c.set_window_position(-2000,0)
    # 登录拿号码
    token=Xunma_login()
    phone=str(Xunma_getphone(token))

    # 发验证码
    Onedrive_signup_send(phone)

    # 收验证码
    result=Xunma_getMessage(token,phone)
    timeout=0

    while result=='Null' or result=='NOTION&单笔充值满 50元送 5%单笔充值满100元送10%自动赠送！上不封顶！[End]':
        time.sleep(5)
        result=Xunma_getMessage(token,phone)
        timeout+=1

        if timeout>5:
            print('timeout!release!')
            Xunma_releasePhone(token,phone)
            c.close()
            return 0
        else:
            print('check..',timeout)

    if result!='Null' and result!='NOTION&单笔充值满 50元送 5%单笔充值满100元送10%自动赠送！上不封顶！[End]':
        verifycode=re.search(r'(?<=\?)\d{4}(?=\?)',result).group()
        # 如果接到了验证码,则提交验证码
        return Onedrive_signup_verify(verifycode)
    return 0


def main_Caoma():
    pid='2171'  # 项目id
    token='9f7df5ea7c4d79a4'
    # 绑定chromedriver
    global c
    c=webdriver.Chrome(executable_path=r'D:\OneDrive\tools\chromedriver.exe')

    # 登录
    CM=Caoma()
    uid,token=CM.login().split('|')
    CM.getUserInfos(uid,token)

    # 拿号码
    mobilenum,token=CM.getMobilenum(pid,uid,token).split('|')

    # 收验证码
    sms_result=CM.getVcodeAndReleaseMobile(pid,uid,token,mobilenum)


def main_Ailezan(url,次数,proxy_status='on'):
    pid='5062'
    Alz=Ailezan()

    login_status,token=Alz.login()
    if str(login_status)=='1':
        pass
    else:
        raise '登录状态错误!'
    # login_status,token=('1','ba659b48-ce56-4577-9f49-4db003742adb')
    Alz.getSummary(token)#查询账号信息

    if proxy_status=='on':
        proxy='127.0.0.1:1080'
        chrome_options=webdriver.ChromeOptions()
        chrome_options.add_argument('--proxy-server=%s'%proxy)
    else:
        chrome_options=None
    if login_status=='1':
        #登录成功,开始搞事情
        #计数器
        succ_times=0
        while succ_times<次数:
            print('--------------当前成功次数:',succ_times)
            # 绑定chromedriver
            global c
            # c=webdriver.Chrome(executable_path=r'D:\DDL DATA\OneDrive\tools\chromedriver.exe')
            c=webdriver.Chrome(executable_path=r'D:\DDL DATA\OneDrive\tools\chromedriver.exe',
                               chrome_options=chrome_options)
            #拿号码
            getmobilenum_status,mobile=Alz.getMobilenum(pid,token).split('|')

            if getmobilenum_status=='1':
                #拿到号码了,请求验证码
                psw='Ha'+str(''.join(random.choices('1234567890qwertyuiopasdfghjklzxcvbnm',k=9)))

                Onedrive_signup_send(url,mobile,psw)
                #todo 确保成功发送验证码了
                #取验证码(等5秒才去取)
                time.sleep(5)
                try:
                    Vcode_status,Vcode=Alz.getVcode(pid,token,mobile).split('|')
                except ValueError and AttributeError:
                    print('获取验证码出错!Valueerror')
                checktimes=0
                while Vcode_status!='1':
                    time.sleep(3)
                    checktimes+=1
                    try:
                        Vcode_status,Vcode=Alz.getVcode(pid,token,mobile).split('|')
                    except:
                        print('获取验证码出错!')
                    if checktimes>=10:#超时次数
                        print('timeout!realease...')
                        Alz.addIgnoreList(pid,token,mobile)
                        c.close()
                        break
                if Vcode_status=='1':
                    print(Vcode)
                    Alz.addIgnoreList(pid,token,mobile)
                    try:
                        verifycode=re.search(r'(?<=\?)\d{4}(?=\?)',Vcode).group()
                    except:
                        print('验证码匹配出错!收到了假的验证码!')
                    else:
                        #提交code
                        #todo 有时候输入验证码之后会退转到'https://signup.live.com/error.aspx?errcode=8001'
                        if Onedrive_signup_verify(verifycode) is True:
                            succ_times+=1
                            writelog(usrname=mobile,psw=psw)
                        print('执行完成!')
                        # c.close()
            else:
                print('获取号码出错了!')

    else:
        print('登录出错了!')
    pass


def main_手动挡():
    global c
    c=webdriver.Chrome(executable_path=r'D:\DDL DATA\OneDrive\tools\chromedriver.exe')
    Onedrive_signup_send(input('mobile:'))
    Onedrive_signup_verify(input('Vcode:'))


def Onedrive_login(url,usrname,psw):
    global c
    proxy='127.0.0.1:1080'
    chrome_options=webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=%s'%proxy)
    c=webdriver.Chrome(executable_path=r'D:\DDL DATA\OneDrive\tools\chromedriver.exe',chrome_options=chrome_options)
    c.get(url)
    #输入账号
    c.find_elements_by_xpath('//*[@id="CredentialsInputPane"]/div[2]/div/div/div[3]/div[2]/div/div[2]/div')[0].click()
    c.find_elements_by_xpath('//*[@id="i0116"]')[0].send_keys('+86'+usrname)
    time.sleep(1)
    c.find_elements_by_xpath('//*[@id="idSIButton9"]')[0].click()
    #输入密码
    getelement('//*[@id="i0118"]').click()
    time.sleep(1)
    getelement('//*[@id="i0118"]').send_keys(psw)
    time.sleep(1)
    getelement('//*[@id="idSIButton9"]').click()
    #如果是新账号,要处理弹出的那俩框
    try:
        getelement('//*[@id="FirstRunDialog-tutorial--0"]/div[4]/button[2]').click()
        time.sleep(1)
        c.find_elements_by_xpath('//*[@id="FirstRunDialog-tutorial--1"]/div[4]/button[2]')[0].click()
        time.sleep(1)
        c.find_elements_by_xpath('//*[@id="FirstRunDialog-tutorial--2"]/div[4]/button[2]')[0].click()
        time.sleep(1)
        print(usrname,'这个账号是新账号!')
        c.find_elements_by_xpath('//*[@id="appRoot"]/div/div[5]/div/div/div/div/div[2]/div[2]/div/div[1]/button')[
            0].click()

    except:
        pass
    c.maximize_window()
    try:
        c.find_elements_by_xpath(
            '//*[@id="appRoot"]/div/div[2]/div[4]/div/div[2]/div[1]/div/div/div[1]/div/div[1]/div/a')[0].click()
    except:
        c.get(c.current_url+'#v=managestorage')


def main_reactive():
    datas='''2017-07-18 16:14|17068978720|Habw56r44ee
2017-07-18 16:17|17091720696|Haf9yuwfg8f
2017-07-18 16:18|17085438124|Hang0h5e05g
2017-07-18 16:20|17168090290|Hac8d7h1srj
2017-07-18 16:20|17168091328|Hax15dr2nvf'''
    datas=datas.split('\n')
    print(datas)
    for data in datas:
        usrname,psw=data.split('|')[1:]
        try:
            Onedrive_login(url,usrname,psw)
        except:
            print(data)


def main_reactive_auto(line):
    #failedlist用于记录失败的
    failedlist=[]
    with open('D://hotmail.txt','r') as file:
        for i in file.readlines()[-line:]:
            usrname,psw=i.strip('\n').split('|')[1:]
            try:
                Onedrive_login(url,usrname,psw)
            except:
                print(i,'出错 ,已加入重试列表!')
                failedlist.append(i)
        file.close()
    if failedlist:
        print('第一轮执行完毕,共{}个,失败{}个! 现在开始执行刚刚失败的!\n这次失败的将在下面打印出来:'.format(line,len(failedlist)))
        for failed in failedlist:
            usrname,psw=failed.strip('\n').split('|')[1:]
            try:
                Onedrive_login(url,usrname,psw)
            except:
                print(i)
                failedlist.append(i)


if __name__=='__main__':
    url='https://onedrive.live.com/?invref=f2b67a4b98b16c35&invscr=90'#小猪哥,下午5点前要求到账
    main_Ailezan(url,2,proxy_status='off')
    main_reactive_auto(2)
