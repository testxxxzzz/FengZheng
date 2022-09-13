# FengZheng (风筝)



```
FengZheng是一款用于权限维持的后门工具。其灵感来源于WannaCry和Cobalt Strike。通过python编写，在尽量仅使用标准库的情况下实现功能。
由于不存在敏感行为及代码，可以规避一些安全检测。本项目属于python新手练习作品，多有缺憾之处请各位谅解，今后会慢慢完善。
```

# 使用方法

```
1、在公网服务器启动teamserver.py
2、将server.py在受害者机器上启动
3、攻击者本地启动client.py，连接公网teamserver进行后门操作
```

# 思路原理

```
整体架构类似于Cobalt Strike，server<-->teamserver<-->client
server则只是一个装载器，通常用于装载反弹shell命令。
常规情况下心跳时间请求teamserver特定端口的web服务，根据web目录判断是否激活以及销毁自身。
```

###### 技术构成

```
1、http请求
2、socket网络编程
3、python文件操作
4、多线程
```

# TODO

```
server快捷添加及隐藏进程
系统清理功能
shell命令远程装载
......
```

# 已完成

```
多用户功能
socket阻塞相关问题
teamserver基础功能
server基础功能
client基础功能
```


# 注意
~~目前该项目仍处于调试开发阶段，存在大量bug，暂时无法实战使用~~

勉强能用了





