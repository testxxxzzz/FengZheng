import socket
import json
from time import sleep


def cserver():
    sk = socket.socket()
    sk.connect(("127.0.0.1", 9000))

# 处理收发数据的逻辑
    pwd = input("请输入您的密码:")
    bytes_msg = pwd.encode()
    sk.send(bytes_msg)

# 接收服务器端发送过来的数据
    res_msg = sk.recv(1024).decode()
    print(res_msg)
    dic_code = json.loads(res_msg)
    if dic_code["code"]:
        print("恭喜你,登录成功")
        while True:
            cmd = input("请输入命令\n")
            cmd = str(cmd)
            if cmd =="add":
                sk.send(bytes(cmd, encoding="utf_8"))
                print("1111")
            elif cmd == 'getlist':
                sk.send(bytes(cmd, encoding="utf_8"))
                print("已执行")
                res_msg = sk.recv(1024).decode()
                print(res_msg)
            elif cmd == 'del':
                sk.send(bytes(cmd, encoding="utf_8"))
                cmd2=input("请输入flag")
                cmd3=str(cmd2)
                sk.send(bytes(cmd3, encoding="utf_8"))
                print("已执行")
            elif cmd=="exit":
                print("3秒钟后退出")
                
                sk.send(bytes(cmd, encoding="utf_8"))
                sleep(3)
                sk.close()
                break
            elif cmd=="test":
                sk.send(bytes(cmd, encoding="utf_8"))
                res_msg = sk.recv(1024).decode()
                print(res_msg)
                # break
            else:
                print("请输入help查看详细命令")
    else:
        print("登录失败")
    sk.close()


cserver()
