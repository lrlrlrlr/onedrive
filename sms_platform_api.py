'接码平台'
import requests
import time


class Ailezan():
    url = 'http://api.hellotrue.com/api/do.php?'

    def __init__(self):
        self.login()

    def login(self, uid='api-c777w00r', psw='209209'):
        '''170723进行了重构'''
        print('')
        self.attempt = 0
        self.login_status = 0
        self.url = Ailezan.url + \
            'action=loginIn&name={}&password={}'.format(uid, psw)
        # print(self.url) #调试用
        while self.login_status != 1:
            if self.attempt > 3:  # 尝试5次
                break
            else:
                self.attempt += 1
            try:
                self.r = requests.get(self.url)
            except BaseException:
                print('requests请求出问题了!')
            else:
                if self.r.status_code == 200:  # 判断是否成功访问
                    try:
                        self.login_status, self.token = self.r.text.split(
                            '|')  # 读取返回数据
                    except BaseException:
                        print('登录返回数据格式不对,请查证:', self.r.text)
                    else:
                        if str(self.login_status) == '1':
                            print('登录成功!')
                            return (self.login_status, self.token)
                        else:
                            print('登录失败!登录情况:', self.r.text)
                else:
                    print('未成功访问,statucode:', self.r.status_code)
            time.sleep(3)

    def getUserInfos(self, uid, token):
        pass

    def get_mobilenumber(self, pid):
        '''170723进行了重构'''
        print('获取账号情况:', end='')
        self.url = Ailezan.url + \
            'action=getPhone&sid={}&token={}'.format(pid, self.token)
        try:
            self.r = requests.get(self.url)
            if self.r.status_code==200:
                mobilenumber_status, mobilenumber = self.r.text.split('|')
                if mobilenumber_status=='1':
                    return mobilenumber
                else:
                    print('mobilenumber_status出错',self.r.text)
        except:
            print('获取账号失败！',self.r.text)
            pass

    def receive_verificationcode(self, pid, mobile):
        '''170723进行了重构'''
        print('获取验证码：', end='')
        self.url = Ailezan.url + \
            'action=getMessage&sid={}&phone={}&token={}'.format(pid, mobile, self.token)
        try:
            self.r = requests.get(self.url)
            if self.r.status_code == 200:
                print(self.r.text)
                verifycode_status, verifycode = self.r.text.split('|')
                if verifycode_status == '1':
                    return verifycode
                else:
                    print('接码平台返回状态出错！',self.r.text)
            else:
                print('status_code error!', self.r.status_code)
        except BaseException:
            print('没有接收到验证码!',self.r.text)
            pass

    def add_ignore_list(self, pid,  mobile):  # 这里可以批量加黑,用','分隔开即可! 因暂不需要 没做这个功能!
        '''170723进行了重构'''
        self.url = Ailezan.url + \
            'action=addBlacklist&sid={}&phone={}&token={}'.format(pid, mobile, self.token)
        try:
            self.r = requests.get(self.url)
            if self.r.status_code == 200:
                print('加黑账号:', self.r.text)
                return self.r.text
        except BaseException:
            pass
        pass

    def getSummary(self, token):
        self.url = Ailezan.url + 'action=getSummary&token={}'.format(token)
        self.r = requests.get(self.url)
        # print(self.r.text.split('|'))
        status, balance, level, 批量取号数, usrtype, _ = self.r.text.split('|')
        print(
            '获取账号信息:balance={},level={},批量取号数={}'.format(
                balance, level, 批量取号数))

    def cancelAllRecv(self, token):
        self.url = Ailezan.url + 'action=cancelAllRecv&token={}'.format(token)
        self.r = requests.get(self.url)
        print('释放所有账号:', self.r.text)


if __name__ == '__main__':
    a = Ailezan()
    a.add_ignore_list('5502','17164357794')
