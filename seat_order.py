# encoding:utf-8
import requests
import datetime
import threading
import time
import sys
import base64
from PIL import Image
from io import BytesIO
from send_Email import send_Email


class seat_order(object):
    def __init__(self, user_name, passwd, seat_id, email):
        self.user_info = [user_name, passwd, seat_id, email]
        self.max_post = True
        self.headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Content-Length": "91",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "210.44.64.139",
            "Origin": "http://210.44.64.139",
            "Referer": "http://210.44.64.139/seat/index.php",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }

        self.thread_lock = threading.Lock()
        self.session = requests.session()
        self.login_data = {"postdata[username]": "", "postdata[password]": "", "postdata[captcha]": ""}
        # days=0设置预约时间（0表示当天，1表示明天......）
        self.order_data = {'order_date': (datetime.datetime.now() + datetime.timedelta(days=0)).strftime("%Y-%m-%d"), 'seat_id': ""}
        self.login_url = "http://210.44.64.139/seat/seatOrderAction.php?action=normalLogin"
        self.order_url = "http://210.44.64.139/seat/seatOrderAction.php?action=addOrderSeat"
        self.captcha_url = "http://210.44.64.139/seat/captcha.php"
        # send_Email（邮箱服务器， 端口号， 发送方邮箱地址， 密码（授权码）， 发送方邮箱地址）
        self.send_email = send_Email("smtp.163.com", 465, "******@163.com", "********", "******@163.com")
        self.login_status_ = ["",1,]

    def login(self, user, passwd):
        true = True
        false = False
        login_status = False
        r_data_json = dict()
        try:
            r_captcha = self.session.get(url=self.captcha_url, headers=self.headers)
            out = BytesIO(r_captcha.content)
            image = Image.open(out)
            image.show()
        except Exception as e:
            print(e)
        self.login_data["postdata[username]"] = str(user)
        self.login_data["postdata[password]"] = str(passwd)
        self.login_data["postdata[captcha]"] = input("Input Captcha:#")
        try:
            r_data = self.session.post(url=self.login_url, data=self.login_data, headers=self.headers)
            r_data.encoding = "utf-8"
            print(r_data.text)
            if r_data.status_code == 200:
                r_data_json = eval(r_data.text.split()[-1])
                login_status = r_data_json["success"]
                print(r_data_json)
        except Exception as e:
            r_data_json["message"] = "连接失败"
            print("Login Error!")
        return login_status, r_data_json["message"]

    def order_seat(self, seat_id, index_i):
        true = True
        false = False
        order_status = False
        r_data_json = dict()
        r_data_json["message"] = "连接失败"
        print("Start----------------------" + str(seat_id))
        self.order_data["seat_id"] = seat_id
        try:
            res = self.session.post(url=self.order_url, data=self.order_data, headers=self.headers)
            res.encoding = "utf-8"
            if res.status_code == 200:
                try:
                    r_data_json = eval(res.text.split()[-1])
                    print(r_data_json)
                    order_status = r_data_json["success"]
                except Exception as e:
                    self.thread_lock.acquire()
                    self.max_post = False
                    self.thread_lock.release()
                #print(e)
                    print("请求上限！")
                if order_status:
                    self.thread_lock.acquire()
                    self.login_status_[index_i] = "yes"
                    self.thread_lock.release()
                if "未登陆" in r_data_json["message"]:
                    self.login_status_[1] = 0
                print(order_status)
        except Exception as e:
            r_data_json["message"] = "连接失败"
            print("Seat_post Error!")
        return order_status, r_data_json["message"]

    def run_thread(self, seat_id, index_i):
        threads = []
        # 创建线程
        try:
            for i in range(6):
                thread = threading.Thread(target=self.order_seat, args=(seat_id, index_i,))
                thread.setDaemon(True)
                threads.append(thread)
        except Exception as e:
            print(e)
        # 启动线程
        try:
            for t in threads:
                if self.login_status_[index_i] != "":
                    break
                t.start()
            for t in threads:
                t.join
        except Exception as e:
            print(e)

    def get_user_data(self):
        return self.user_info

    def s_hint(self):
        self.send_email.send(self.user_info[3], "到期提示！", "你的账户明天即将到期，如需继续使用请及时续期！!")

    def run(self):
        self.login_status_[1] = 1
        true = True
        false = False
        index_i = 0
        user = list(self.get_user_data())
        self.login_status_.append("")
        print(user[3])
        status, msg = self.login(str(user[0]), str(user[1]))
        while not status:
            status, msg = self.login(str(user[0]), str(user[1]))
        if status:
            self.send_email.send(str(user[3]), "启动提示！", "Success!" + user[0])
            print("Login成功！")
        while True:
            self.thread_lock.acquire()
            if self.login_status_[1] == 0:
                self.login(str(user[0]), str(user[1]))
                self.login_status_[1] = 1
            if self.login_status_[index_i] != "":
                if self.login_status_[index_i] == "yes":
                    self.login_status_[index_i] = "no"
                    self.send_email.send(str(user[3]), "预约成功提示！", "Success!" + user[0])
                break
            self.thread_lock.release()
            self.run_thread(user[2], index_i)
            if self.max_post:
                time.sleep(2)
            else:
                self.max_post = True
                time.sleep(30)
        return 0


if __name__ == '__main__':
    user_name = "20200202001"
    passwd = "000000"
    seat_id = "001"
    email = "***@163.com"
    stop_time = datetime.datetime.now().strftime("%Y-%m-%d")
    try:
        user_name = sys.argv[1]
        passwd = sys.argv[2]
        seat_id = sys.argv[3]
        email = sys.argv[4]
        stop_time = sys.argv[5]
    except Exception as e:
        print(e)
    stop_dt = datetime.datetime.strptime(str(stop_time), "%Y-%m-%d").date()
    now_dt = datetime.datetime.now().date()
    if now_dt < stop_dt:
        so = seat_order(user_name, passwd, seat_id, email)
        so.run()
    elif now_dt == stop_dt:
        so = seat_order(user_name, passwd, seat_id, email)
        try:
            so.s_hint()
        except:
            print("ERROR")
        so.run()
        
