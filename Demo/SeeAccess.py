import json
import re
import time
import logging
import sys
from socket import socket, AF_INET, SOCK_STREAM
import threading

'''
    log_format  main '$remote_addr - $remote_user [$time_local] "$request" '
                      '"$status" $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for" '
                        '"$request_time" $upstream_response_time';
'''


point = 0
config = json.loads(open(r'checkFile.json', encoding='utf-8').read())
file = config["file"]
monitor = config["monitor"]
if monitor == -1:
    sys.exit(0)
outTime = config["outTime"]
HOST = config["sendIP"]
PORT = config["sendPort"]
ADDR = (HOST, PORT)


# 创建一个logger
logger = logging.getLogger('listen')
logger.setLevel(logging.DEBUG)

# 创建一个handler，用于写入日志文件
fh = logging.FileHandler('see.log')
fh.setLevel(logging.DEBUG)

# 定义handler的输出格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(fh)


# 读取文件入口
def entrance():
    print("检索更新的请求日志中······")
    replaceFileDate()
    global point
    f = open(file, encoding='utf-8')
    f.seek(point)
    lines = f.readlines()
    point = f.tell()
    if len(lines) > 0:
        errorMsg = ''
        for line in lines:
            one = checkURLResponse(line)
            if len(one) > 0:
                errorMsg = errorMsg + '**************\n' + one + '\n'
        if len(errorMsg) > 0:
            sendMSG('出现响应过慢，请关注：\n\n' + errorMsg)


# 替换文件名中的时间
def replaceFileDate():
    global file
    file = str(file).replace('$date', time.strftime('%Y-%m-%d-%H', time.localtime(time.time())))


# 消息推送
def sendMSG(msg):
    try:
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        tcpCliSock.connect(ADDR)
        data = {"type": "forward", "monitor": monitor, "msg": msg}
        tcpCliSock.send(json.dumps(data).encode())
        tcpCliSock.close()
    except Exception as r:
        logger.error(str(r) + '--------sendMSG')
        print('请求失败，继续请求')


# 心跳推送
def selfHeart():
    try:
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        tcpCliSock.connect(ADDR)
        data = {"type": "heart", "monitor": monitor}
        tcpCliSock.send(json.dumps(data).encode())
        tcpCliSock.close()
    except Exception as r:
        logger.error(str(r) + '--------selfHeart')
    finally:
        threading.Timer(60, selfHeart, ()).start()


# 监控每一行的请求时间是否超出配置的阈值
def checkURLResponse(line):
    pattern = re.compile('''(?<=").*?(?=")''')
    result = pattern.findall(line)
    times = float(result[len(result) - 1])
    if times > outTime:
        getTime = re.compile('''(?<=\[).*?(?=\])''')
        sendTime = getTime.findall(line)
        return result[0] + '\n响应状态： '+result[2]+'\n响应时间：' + str(times) + '秒\n请求时间：' + sendTime[0]
    else:
        return ''


# start 方法
def start():
    try:
        do = threading.Thread(target=entrance, )
        do.start()
        while do.is_alive():
            time.sleep(0.5)
    except Exception as r:
        logger.error(str(r))
    finally:
        threading.Timer(10, start, ()).start()


# 初始化文件指针到最后
def initFile():
    print("初始化日志文件的指针位置")
    replaceFileDate()
    global point
    f = open(file, encoding='utf-8')
    f.seek(point)
    lines = f.readlines()
    point = f.tell()
    del lines


initFile()
threading.Thread(target=selfHeart, ).start()
start()
sendMSG(' nginx 请求监控启动成功')
