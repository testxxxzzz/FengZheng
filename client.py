import socket
import json


def cserver():
    sk = socket.socket()
    sk.connect(("127.0.0.1", 9000))

# 处理收发数据的逻辑
    pwd = input("请输入您的密码:")
    bytes_msg = pwd.encode()
    sk.send(bytes_msg)

# 接收服务器端发送过来的数据
    res_msg = sk.recv(1024).decode()
    #print(res_msg)
    dic_code = json.loads(res_msg)
    if dic_code["code"]:
        print("welcome FengZheng")
        while True:
            cmd = input("------请输入命令------\n\n\n")
            cmd = str(cmd)
            if cmd == "add":
                sk.send(bytes(cmd, encoding="utf_8"))
                print("添加成功")
            elif cmd == 'getlist':
                sk.send(bytes(cmd, encoding="utf_8"))
                print("\n已执行")
                res_msg = sk.recv(1024).decode()
                print(res_msg)
            elif cmd == 'del':
                sk.send(bytes(cmd, encoding="utf_8"))
                cmd2 = input("请输入flag\n")
                cmd3 = str(cmd2)
                sk.send(bytes(cmd3, encoding="utf_8"))
                print("\n已执行")
            elif cmd == 'alive':
                sk.send(bytes(cmd, encoding="utf_8"))
                cmd2 = input("请输入要激活的flag\n")
                cmd3 = str(cmd2)
                sk.send(bytes(cmd3, encoding="utf_8"))
                print("\n已执行")
            elif cmd == "exit":
                print("\n您已离开控制器")

                sk.send(bytes(cmd, encoding="utf_8"))
                #sleep(5)
                sk.close()
                break
            elif cmd == "test":
                sk.send(bytes(cmd, encoding="utf_8"))
                res_msg = sk.recv(1024).decode()
                print(res_msg)
                # break
            elif cmd == "help":
                print("add:添加flag \n")
                print("getlist:获取flag列表 \n")
                print("del:删除flag \n")
                print("exit:退出 \n")
                print("test:测试 \n")
            else:
                print("请输入help查看详细命令")
    else:
        print("\n登录失败\n")
    sk.close()


cserver()
