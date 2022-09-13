import os
import urllib.request
from time import sleep

baseurl = "127.0.0.1:8000"
flag = input("请输入URL：")
time = float(input("心跳时间："))
payload = "whoami"

# 检测标准码


def rt(flag):
    try:
        response = urllib.request.urlopen(
            'http://'+baseurl+'/server/'+flag, timeout=3).code
        html = response
        print(html)
        return html
    except urllib.error.HTTPError as html:
        return "404"

# 检测exit码


def live():
    try:
        response2 = urllib.request.urlopen(
            'http://'+baseurl+'/server/'+flag+'alive', timeout=3).code
        html = response2
        # 获取返回码
        print(html)
        return html
    except urllib.error.URLError as html:
        return "404"


while True:
    t1 = rt(flag)
    print("t1的值是", t1)
    # sleep(time*3600)
    sleep(time)

    if t1 == 200:
        print("标准码200，程序睡眠")
    else:
        print("标准码是200，进入第二流程")
        t2 = live()
        print("t2的值是", t2)
        if t2 == 200:
            print("EXIT码200，程序唤醒")
        else:
            print("EXIT404，程序自杀")
            # 获取文件名
            filename = os.path.basename(__file__)
            # 删除本身
            # os.remove("./"+filename)
            print("./"+filename)
            break
