import os
import random
import shutil
import socket
import json
import http.server
import socketserver
from tracemalloc import stop

# flag = "X8KOy4"
baseurl = "127.0.0.1"
# flag=input("请输入URL：")
# time=float (input("心跳时间："))
# payload = "whoami"


def generate_random_str(s=6):
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    for i in range(s):
        random_str += base_str[random.randint(0, 61)]
    return random_str


def add():
    r = generate_random_str()

    os.mkdir(r)
    with open("log", 'a+') as f:
        f.write('flag:'+r+'    target:'+baseurl+'\n')
    print("已创建：", r)


def pwd():
    r2 = generate_random_str(12)
    with open("pwd", 'w') as p:
        p.write(r2)
    print("您的TeamServer密码为：", r2, "请妥善保存！")


def delete(flag):
    with open('log', 'r') as f:
        with open('log.bak', 'w') as g:
            for line in f.readlines():
                if flag not in line:
                    g.write(line)
        shutil.move('log.bak', 'log')
    os.rename(flag, flag+"exit")

    print("已删除：")


def getlist():
    with open("log", "r") as f:
        txt = f.read()
    # print(txt)
    return txt

def httpserver():
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()


def tserver():
    sk = socket.socket()
    sk.bind(("127.0.0.1", 9000))
    print("正在启动服务器......\n")
    sk.listen()
    print("启动成功")
    #pwd() #随机生成密码
    conn, addr = sk.accept()
    msg = conn.recv(1024).decode()
    sign = False
    with open("pwd", "r") as fp:
        for line in fp:
            lpwd = line
            if msg == lpwd:
                res = {"code": 1}
                res_msg = json.dumps(res).encode()
                conn.send(res_msg)
                sign = True
            if sign == False:
                res = {"code": 0}
                print(res)
                res_msg = json.dumps(res).encode()
                conn.send(res_msg)
            while True:
                # try:
                msg = conn.recv(1024).decode()
                # except:
                #     pass
                # else:
                #     print("位置三：",msg)
                #     msg="exit"
                #     break
                
                while True:
                    if msg == "getlist":
                        lists=getlist()
                        conn.send(bytes( lists.encode()))
                    elif msg == "add":
                        add()
                        break
                    elif msg == "del":
                        # print("请输入目标值")  ##删除功能需要修改
                        msg2 = conn.recv(1024).decode()
                        print(msg2)
                        delete(str(msg2))
                        break
                    elif msg == "test":
                        def excmd():
                            if msg == "test":
                                print("ok")
                                conn.send(bytes( "ok".encode()))
                                return "ok"
                        excmd()
                        break
                    elif msg == "exit":
                        print("11111111111111")
                        conn.close()
                        print("22222222222")
                        # sk.close()
                        # break
                        # continue
                                     
                        #！！！！！！！！！解决客户端终止后无法再次连接的问题
                    # break
                    continue


# add()
# delete()
# getlist()
# pwd()
# httpserver()
tserver()

