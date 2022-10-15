import json
import time
import traceback

import requests
import random

# -----------------------配置区-----------------------


# 账号
USER = ""
# 密码
PASS = ""
# 需要续费的套餐，如果套餐id是111和112，那么就是renewalPackage = [111,112]
# 如果是111,那么就是renewalPackage = [111]
# 默认月续费，不可变更
renewalPackage = []


# -----------------------配置区-----------------------


class LiuYiCdn:
    def __init__(self):
        self.liuyihref = "cdn-user.61cloud.net"
        self.loginhref = "/login"
        self.gettchref = "/user-packages"
        self.xfhref = "/user-packages/"
        self.ip = self.camouflage_ip()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36",
            "origin": "http://" + self.liuyihref,
            "referer": "http://" + self.liuyihref + "/console",
            "Host": self.liuyihref,
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json; charset=utf-8",
            "Client-Ip": self.ip,
            "X-Forwarded-For": self.ip,
            "x-forwarded-for": self.ip,
            "Remote_Addr": self.ip,
            "x-remote-IP": self.ip,
            "x-remote-ip": self.ip,
            "x-client-ip": self.ip,
            "x-client-IP": self.ip,
            "X-Real-IP": self.ip,
            "client-IP": self.ip,
            "x-originating-IP": self.ip,
            "x-remote-addr": self.ip,
        }
        self.access_token = None

    def login(self):
        res = None
        success = False
        attempts = 0
        submit = {'account': USER, 'password': PASS, 'code': "", 'captcha': ""}
        while not success and attempts < 10:
            try:
                res = requests.post("http://" + self.liuyihref + self.loginhref, data=json.dumps(submit),
                                    headers=self.headers)
                success = True
                break
            except:
                # traceback.print_exc()
                time.sleep(1)
                attempts += 1
                print("登陆重试中 第" + str(attempts) + "次")
                if attempts > 10:
                    print("登陆重试次数超过了10次")
        if not success:
            self.access_token = None
            return
        res_txt = res.content.decode()
        res_json = None
        try:
            res_json = json.loads(res_txt)
        except:
            print("登陆错误")
        if "msg" in res_json and res_json['msg'] != "登录成功!":
            print("账号密码错误")
            return
        print("61cdn登陆成功")
        self.access_token = res_json['data']['access_token']

    def renew(self):
        self.login()
        headers = self.headers
        headers['access-token'] = self.access_token
        submit = {"duration": "month"}
        if self.access_token is None:
            print("你还没有登陆，不能续费")
            return
        for i in renewalPackage:
            res = None
            success = False
            attempts = 0
            while not success and attempts < 10:
                try:
                    res = requests.put("http://" + self.liuyihref + self.xfhref + str(i), headers=headers, data=json.dumps(submit))
                    success = True
                    break
                except:
                    # traceback.print_exc()
                    time.sleep(1)
                    attempts += 1
                    print("续费重试中 第" + str(attempts) + "次")
                    if attempts > 10:
                        print("续费重试次数超过了10次")
            res_txt = res.content.decode()
            res_json = None
            if success:
                try:
                    res_json = json.loads(res_txt)
                    if "code" in res_json and res_json['code'] == 0:
                        print("成功续费：" + str(i) + " 套餐")
                    else:
                        # print(res_txt)
                        print("续费：" + str(i) + " 套餐失败1,原因：" + res_json['msg'])
                except:
                    print("续费：" + str(i) + " 套餐异常")

            else:
                print("续费：" + str(i) + " 套餐失败2")

    def camouflage_ip(self):  # 暂时只能伪装电信ip,伪装其他地区ip更改106.84.
        return "106.84." + str(random.randint(146, 254)) + "." + str(random.randint(1, 254))


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    # 只能调用 .renew()，其余为内部方法
    liuyi = LiuYiCdn()
    liuyi.renew()
