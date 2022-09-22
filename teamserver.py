import datetime
import os
import random
import shutil
import socket
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
from functools import partial
import argparse
from time import sleep


ts_pool = []
baseurl = "0.0.0.0"  # teamserver服务启动地址
HTTP_PORT = 8000  # http服务端口
tserver_port = 9000  # teamserver端口


def parse_args():
    parse = argparse.ArgumentParser()
    parse.add_argument("-hp", "--hport", type=int,
                       default=8000, help="http server port")
    parse.add_argument("-tp", "--tport", type=int,
                       default=9000, help="teamserver port")
    parse.add_argument("-b", "--baseurl", type=str,
                       default="0.0.0.0", help="teamserver listen ip")
    args = parse.parse_args()
    return args


def generate_random_str(s=6):
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    for i in range(s):
        random_str += base_str[random.randint(0, 61)]
    return random_str


def add(targets, r):

    # 创建名为r的空文件
    with open('./server/'+r, 'a+') as f:
        f.write("")
    print("已创建：", r)
    with open("log", 'a+') as f:
        f.write('flag:'+r+'    target:'+targets+'\n')
    print("已写入log：", r)
    return r
    # return r
    # create(r, time, payload, baseurl)
    # print("已生成新的server.py文件")


def pwd():
    r2 = generate_random_str(12)
    with open("pwd", 'w') as p:
        p.write(r2)
    print("您的TeamServer密码为：", r2, "请妥善保存！\n")
# 激活server


def alive(flag):

    with open("log", 'r') as f:
        for line in f.readlines():
            if flag in line:
                # 创建flagalive文件
                os.rename('./server/'+flag, './server/'+flag+"alive")
                print("已激活：", flag)
                return "1"
        return "0"


def delete(flag):
    # 检测文件是否存在
    if os.path.exists('./server/'+flag):
        os.remove('./server/'+flag)
        print("已删除未激活的server：", flag+"\n")
        # 删除log中包含flag的行
        with open("log", 'r') as f:
            with open("log.bak", 'w') as g:
                for line in f.readlines():
                    if flag not in line:
                        g.write(line)
        shutil.move("log.bak", "log")
        print("已删除log中的记录：", flag+"\n")

    elif os.path.exists('./server/'+flag+"alive"):
        # 删除server文件夹下的flag文件
        os.remove('./server/'+flag+"alive")
        print("已删除：", flag+"\n")
    else:
        print("没有存在的server，可能输入了异常字符！\n")


def getlist():
    with open("log", "r") as f:
        txt = f.read()
        if txt == "":
            return "暂无数据"
    return txt


def httpserver(HTTP_PORT):

    Handler = partial(SimpleHTTPRequestHandler, directory="./server")
    httpd = HTTPServer((baseurl, HTTP_PORT), Handler)
    print("http服务已启动，端口为：", HTTP_PORT)
    print("\n")
    httpd.serve_forever()

    # a=socket.gethostbyname(socket.gethostname())
    # print("访问http服务的ip为：",a)


def command(conn):
    while True:
        msg = conn.recv(1024).decode()
        if msg == "list":
            lists = getlist()
            conn.send(bytes(lists.encode()))
            # 清空msg
            msg = ""
            continue
        elif msg == "add":
            r = generate_random_str()
            targets = conn.recv(1024).decode()
            add(targets, r)
            conn.send(bytes(r.encode()))
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

            ifalive = alive(msg2)
            # print(ifalive)
            conn.send(bytes(str(ifalive).encode()))
            msg = ""
            continue

        elif msg == "exit":
            print("一个用户退出了服务器", datetime.datetime.now())
            conn.close()
            break


def tserver(addr, tserver_port):

    sk = socket.socket()
    sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sk.bind((addr, tserver_port))

    print("\n正在启动服务器......\n")
    sk.listen()

    print("teamserver服务器已启动，端口为：", tserver_port)
    print("\n")
    pwd()  # 随机生成密码

    while True:

        conn, addr = sk.accept()

        msg = conn.recv(1024).decode()
        print(msg)
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


if __name__ == "__main__":
    args = parse_args()
    hport = args.hport
    tport = args.tport
    # print(hport)
    # print(tport)
    t = threading.Thread(target=tserver, args=(baseurl, tport,))
    t2 = threading.Thread(target=httpserver, args=(hport,))
    t2.start()
    # 获取访问http服务的ip

    t.start()


sleep(2)
print("所有服务器启动完成\n")
# 检查是否存在log文件,不存在则创建
if not os.path.exists("./log"):
    print("log文件不存在，正在创建\n")
    with open("log", "w") as f:
        f.write("")
    print("log文件创建完成\n")
# 检查是否存在server文件夹,不存在则创建
if not os.path.exists("./server"):
    print("server文件夹不存在，正在创建\n")
    os.mkdir("./server")
    print("server文件夹创建完成\n")
else:
    print("初始化完成，可以使用了\n")


# 如果输入exit则退出所有进程
while True:
    try:
        exit_cmd = input("\n等待退出命令....\n\n输入exit或ctrl+c退出\n")
        if exit_cmd == "exit":
            os._exit(0)
        else:
            continue
    except KeyboardInterrupt:
        os._exit(0)
