# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import subprocess, shlex
import csv
import re
import time
import pandas as pd
import threading

# python调用windows command line时，如果cmd有返回，就会遇到输出乱码的情况，需要更改一下cmd的编码方式：
os.system('chcp 65001')

class myThread (threading.Thread):
    def __init__(self, threadID, name, skiprows,nrows,writer):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.skiprows = skiprows
        self.nrows = nrows
        self.writer = writer
    def run(self):
        print ("开启线程： " + self.name)
        process_muti_thread(self.skiprows, self.nrows, self.writer)

#验证是否是ipv6地址
def is_ipv6(ip):
    # 验证ipv6地址结构的正则表达式
    p = re.compile('^((([0-9A-Fa-f]{1,4}:){7}[0-9A-Fa-f]{1,4})|(([0-9A-Fa-f]{1,4}:){1,7}:)|(([0-9A-Fa-f]{1,4}:){6}:[0-9A-Fa-f]{1,4})|(([0-9A-Fa-f]{1,4}:){5}(:[0-9A-Fa-f]{1,4}){1,2})|(([0-9A-Fa-f]{1,4}:){4}(:[0-9A-Fa-f]{1,4}){1,3})|(([0-9A-Fa-f]{1,4}:){3}(:[0-9A-Fa-f]{1,4}){1,4})|(([0-9A-Fa-f]{1,4}:){2}(:[0-9A-Fa-f]{1,4}){1,5})|([0-9A-Fa-f]{1,4}:(:[0-9A-Fa-f]{1,4}){1,6})|(:(:[0-9A-Fa-f]{1,4}){1,7})|(([0-9A-Fa-f]{1,4}:){6}(\\d|[1-9]\\d|1\\d{2}|2[0-4]\\d|25[0-5])(\\.(\\d|[1-9]\\d|1\\d{2}|2[0-4]\\d|25[0-5])){3})|(([0-9A-Fa-f]{1,4}:){5}:(\\d|[1-9]\\d|1\\d{2}|2[0-4]\\d|25[0-5])(\\.(\\d|[1-9]\\d|1\\d{2}|2[0-4]\\d|25[0-5])){3})|(([0-9A-Fa-f]{1,4}:){4}(:[0-9A-Fa-f]{1,4}){0,1}:(\\d|[1-9]\\d|1\\d{2}|2[0-4]\\d|25[0-5])(\\.(\\d|[1-9]\\d|1\\d{2}|2[0-4]\\d|25[0-5])){3})|(([0-9A-Fa-f]{1,4}:){3}(:[0-9A-Fa-f]{1,4}){0,2}:(\\d|[1-9]\\d|1\\d{2}|2[0-4]\\d|25[0-5])(\\.(\\d|[1-9]\\d|1\\d{2}|2[0-4]\\d|25[0-5])){3})|(([0-9A-Fa-f]{1,4}:){2}(:[0-9A-Fa-f]{1,4}){0,3}:(\\d|[1-9]\\d|1\\d{2}|2[0-4]\\d|25[0-5])(\\.(\\d|[1-9]\\d|1\\d{2}|2[0-4]\\d|25[0-5])){3})|([0-9A-Fa-f]{1,4}:(:[0-9A-Fa-f]{1,4}){0,4}:(\\d|[1-9]\\d|1\\d{2}|2[0-4]\\d|25[0-5])(\\.(\\d|[1-9]\\d|1\\d{2}|2[0-4]\\d|25[0-5])){3})|(:(:[0-9A-Fa-f]{1,4}){0,5}:(\\d|[1-9]\\d|1\\d{2}|2[0-4]\\d|25[0-5])(\\.(\\d|[1-9]\\d|1\\d{2}|2[0-4]\\d|25[0-5])){3}))$')
    if p.match(ip):
        return True
    else:
        return False

def check_ipv6_deployed(domain_url):
    print("查询", domain_url, "的ipv6地址：",end="")
    cmd = "nslookup -query=AAAA " + domain_url + " 2001:4860:4860::64"
    process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, shell=True)
    result = process.stdout.read().decode("gbk")
    # print(result.replace('\r', '').replace('\n', '').replace('\t', '').split(" "))
    last_col = result.replace('\r', '').replace('\n', '').replace('\t', '').split(" ")[-1]

    if (is_ipv6(last_col)):
        # print("The domain has ipv6 deployed.")
        print(last_col)
        return last_col
    else:
        # print("Ipv6 is not yet deployed for this domain.")
        print("not yet deployed Ipv6.")
        return None

def check_ipv4(domain_url):
    print("查询", domain_url, "的ipv4地址：", end="")
    cmd = "nslookup -query=A " + domain_url
    process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, shell=True)
    result = process.stdout.read().decode("gbk")
    # print(result.replace('\r', '').replace('\n', '').replace('\t', '').split(" "))
    last_col = result.replace('\r', '').replace('\n', '').replace('\t', '').split(" ")[-1]
    print(last_col)
    return last_col

def process_muti_thread(skiprows,nrows,writer):
    df = pd.read_csv('top-1m.csv', skiprows=skiprows, nrows=nrows)
    # print(df)
    for index, r in df.iterrows():  # 遍历每一行
        domain_url = r[1]
        ipv6 = check_ipv6_deployed(domain_url)
        if (ipv6 == None):
            continue
        ipv4 = check_ipv4(domain_url)
        # 获取锁，用于线程同步
        threadLock.acquire()
        writer.writerow([domain_url, ipv4, ipv6])
        # 释放锁，开启下一个线程
        threadLock.release()

#用不同的DNS服务器尝试比较网站是否返回IPv6地址以及返回IPv6地址的区别
if __name__ == '__main__':
    # df = pd.read_csv('top-1m.csv', skiprows=687191, nrows=7)
    # print(df)
    # pass
    with open("domain_v4v6_info.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        # 先写入column_name
        writer.writerow(["domain", "ipv4", "ipv6"])

        threadLock = threading.Lock()
        threads = []

        total_lines = len(open("top-1m.csv").readlines())
        # 创建50个新线程,每个线程处理tasks行
        tasks = int(total_lines/50)
        s=0
        n=tasks
        time_start = time.time()
        for i in range(0,50):
            thread = myThread(i+1, "Thread-"+str(i+1), skiprows= s , nrows= n, writer=writer)
            s = s+tasks
            n = n+tasks
            # 开启新线程
            thread.start()
            # 添加线程到线程列表
            threads.append(thread)

        # 等待所有线程完成
        for t in threads:
            t.join()
        time_end = time.time()
        print('time cost:', time_end - time_start, 's')
        print("退出主线程")
        # with open('top-1m.csv', 'r') as f:
        #     reader = csv.reader(f)
        #     time_start = time.time()
        #     for row in reader:
        #         domain_url = row[1]
        #         # 测量在这些热门域名中有多少部署了IPv6
        #         ipv6 = check_ipv6_deployed(domain_url)
        #         if(ipv6==None):
        #             continue
        #         ipv4 = check_ipv4(domain_url)
        #         writer.writerow([domain_url,ipv4,ipv6])
        #         # 主要包括两个方面的性能：完成与网站地址建立连接的速度，传输完整页面的速度。分别完成对网站IPv4地址和IPv6地址的性能对比分析。
        #         # cmd = "nslookup -query=AAAA " + domain_url + " 2001:4860:4860::64"
        #         # process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, shell=True)
        #         # result = process.stdout.read().decode("gbk")
        #          discord.com
        #
        #         # 判断相同网站在通过IPv6访问与IPv4访问，页面内容的差异度问题
        #         # import urllib.request
        #         # req = urllib.request.Request("http://www."+domain_url)
        #         # resp = urllib.request.urlopen(req)
        #         # data = resp.read().decode('utf-8')
        #         #
        #         # print(data)
        #         #调试10个
        #         if(int(row[0])>10):
        #             break
        #     time_end = time.time()
        #     print('time cost:', time_end - time_start, 's')
    # os.system(cmd)
    # process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, shell=True)
    # # print(process.stdout.read().decode("gbk"))  # 将管道的内容读取出来。
    # result = process.stdout.read().decode("gbk")
    # print(result.split(" "))