#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2020/12/2 16:17
# @Author: XiangyuTang
# @File  : Test_connect_speed.py

# pip3 install pycurl
import pycurl
from io import BytesIO,StringIO
import re
import subprocess, shlex
import pandas as pd
import os
import csv

#验证是否是ipv6地址
def is_ipv6(ip):
    # 验证ipv6地址结构的正则表达式
    p = re.compile('^((([0-9A-Fa-f]{1,4}:){7}[0-9A-Fa-f]{1,4})|(([0-9A-Fa-f]{1,4}:){1,7}:)|(([0-9A-Fa-f]{1,4}:){6}:[0-9A-Fa-f]{1,4})|(([0-9A-Fa-f]{1,4}:){5}(:[0-9A-Fa-f]{1,4}){1,2})|(([0-9A-Fa-f]{1,4}:){4}(:[0-9A-Fa-f]{1,4}){1,3})|(([0-9A-Fa-f]{1,4}:){3}(:[0-9A-Fa-f]{1,4}){1,4})|(([0-9A-Fa-f]{1,4}:){2}(:[0-9A-Fa-f]{1,4}){1,5})|([0-9A-Fa-f]{1,4}:(:[0-9A-Fa-f]{1,4}){1,6})|(:(:[0-9A-Fa-f]{1,4}){1,7})|(([0-9A-Fa-f]{1,4}:){6}(\\d|[1-9]\\d|1\\d{2}|2[0-4]\\d|25[0-5])(\\.(\\d|[1-9]\\d|1\\d{2}|2[0-4]\\d|25[0-5])){3})|(([0-9A-Fa-f]{1,4}:){5}:(\\d|[1-9]\\d|1\\d{2}|2[0-4]\\d|25[0-5])(\\.(\\d|[1-9]\\d|1\\d{2}|2[0-4]\\d|25[0-5])){3})|(([0-9A-Fa-f]{1,4}:){4}(:[0-9A-Fa-f]{1,4}){0,1}:(\\d|[1-9]\\d|1\\d{2}|2[0-4]\\d|25[0-5])(\\.(\\d|[1-9]\\d|1\\d{2}|2[0-4]\\d|25[0-5])){3})|(([0-9A-Fa-f]{1,4}:){3}(:[0-9A-Fa-f]{1,4}){0,2}:(\\d|[1-9]\\d|1\\d{2}|2[0-4]\\d|25[0-5])(\\.(\\d|[1-9]\\d|1\\d{2}|2[0-4]\\d|25[0-5])){3})|(([0-9A-Fa-f]{1,4}:){2}(:[0-9A-Fa-f]{1,4}){0,3}:(\\d|[1-9]\\d|1\\d{2}|2[0-4]\\d|25[0-5])(\\.(\\d|[1-9]\\d|1\\d{2}|2[0-4]\\d|25[0-5])){3})|([0-9A-Fa-f]{1,4}:(:[0-9A-Fa-f]{1,4}){0,4}:(\\d|[1-9]\\d|1\\d{2}|2[0-4]\\d|25[0-5])(\\.(\\d|[1-9]\\d|1\\d{2}|2[0-4]\\d|25[0-5])){3})|(:(:[0-9A-Fa-f]{1,4}){0,5}:(\\d|[1-9]\\d|1\\d{2}|2[0-4]\\d|25[0-5])(\\.(\\d|[1-9]\\d|1\\d{2}|2[0-4]\\d|25[0-5])){3}))$')
    if p.match(ip):
        return True
    else:
        return False

#在本例中使用默认DNS获取IPv6地址
def check_ipv6_deployed(domain_url):
    # print("查询", domain_url, "的ipv6地址：",end="")
    cmd = "nslookup -query=AAAA " + domain_url #+ " 2001:4860:4860::64"
    process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, shell=True)
    result = process.stdout.read().decode("gbk")
    # print(result.replace('\r', '').replace('\n', '').replace('\t', '').split(" "))
    last_col = result.replace('\r', '').replace('\n', '').replace('\t', '').split(" ")[-1]

    if (is_ipv6(last_col)):
        # print("The domain has ipv6 deployed.")
        # print(last_col)
        return last_col
    else:
        # print("Ipv6 is not yet deployed for this domain.")
        # print("not yet deployed Ipv6.")
        return None

def check_ipv4(domain_url):
    # print("查询", domain_url, "的ipv4地址：", end="")
    cmd = "nslookup -query=A " + domain_url
    process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, shell=True)
    result = process.stdout.read().decode("gbk")
    # print(result.replace('\r', '').replace('\n', '').replace('\t', '').split(" "))
    last_col = result.replace('\r', '').replace('\n', '').replace('\t', '').split(" ")[-1]
    # print(last_col)
    return last_col

def test_website(url):
    c = pycurl.Curl()
    buffer = BytesIO()  # 创建缓存对象
    html = buffer

    c.setopt(c.WRITEDATA, buffer)  # 设置资源数据写入到缓存对象
    c.setopt(c.URL, url)  # 指定请求的URL
    c.setopt(c.MAXREDIRS, 5)  # 指定HTTP重定向的最大数
    # 连接超时设置
    c.setopt(pycurl.CONNECTTIMEOUT, 2)
    c.setopt(pycurl.TIMEOUT, 300)
    # 模拟浏览器
    c.setopt(pycurl.USERAGENT, "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)")
    c.setopt(pycurl.WRITEFUNCTION, html.write)
    c.perform()  # 执行

    http_code = c.getinfo(pycurl.HTTP_CODE)  # 返回的HTTP状态码
    dns_resolve = c.getinfo(pycurl.NAMELOOKUP_TIME)  # DNS解析所消耗的时间
    http_conn_time = c.getinfo(pycurl.CONNECT_TIME)  # 建立连接所消耗的时间
    http_pre_trans = c.getinfo(pycurl.PRETRANSFER_TIME)  # 从建立连接到准备传输所消耗的时间
    http_start_trans = c.getinfo(pycurl.STARTTRANSFER_TIME)  # 从建立连接到传输开始消耗的时间
    http_total_time = c.getinfo(pycurl.TOTAL_TIME)  # 传输结束所消耗的总时间
    http_size_download = c.getinfo(pycurl.SIZE_DOWNLOAD)  # 下载数据包大小
    http_size_upload = c.getinfo(pycurl.SIZE_UPLOAD)  # 上传数据包大小
    http_header_size = c.getinfo(pycurl.HEADER_SIZE)  # HTTP头部大小
    http_speed_downlaod = c.getinfo(pycurl.SPEED_DOWNLOAD)  # 平均下载速度
    http_speed_upload = c.getinfo(pycurl.SPEED_UPLOAD)  # 平均上传速度
    http_redirect_time = c.getinfo(pycurl.REDIRECT_TIME)  # 重定向所消耗的时间
    http_content_type = c.getinfo(c.CONTENT_TYPE)

    print('HTTP响应状态： %d' % http_code)
    print('DNS解析时间：%.2f ms' % (dns_resolve * 1000))
    print('建立连接时间： %.2f ms' % (http_conn_time * 1000))
    print('准备传输时间： %.2f ms' % (http_pre_trans * 1000))
    print("传输开始时间： %.2f ms" % (http_start_trans * 1000))
    print("传输结束时间： %.2f ms" % (http_total_time * 1000))
    print("完整传输时间： %.2f ms" % ((http_total_time * 1000)-(http_start_trans * 1000)))
    print("重定向时间： %.2f ms" % (http_redirect_time * 1000))
    print("上传数据包大小： %d bytes/s" % http_size_upload)
    print("下载数据包大小： %d bytes/s" % http_size_download)
    print("HTTP头大小： %d bytes/s" % http_header_size)
    print("平均上传速度： %d k/s" % (http_speed_upload / 1024))
    print("平均下载速度： %d k/s" % (http_speed_downlaod / 1024))
    print("网页 Content-type:", http_content_type)
    print("网页内容：", html.getvalue())

    conn_time = http_conn_time * 1000
    transfer_time = (http_total_time * 1000)-(http_start_trans * 1000)
    page_content = str(html.getvalue().strip())
    return conn_time,transfer_time,page_content

if __name__ == '__main__':

    # python调用windows command line时，如果cmd有返回，就会遇到输出乱码的情况，需要更改一下cmd的编码方式：
    os.system('chcp 65001')
    # 考虑到Ipv6地址可能是临时地址，因此在测试连接速度的时候重新获取一下ipv4,v6地址
    df = pd.read_csv('top-1m.csv')
    with open("v4v6_comparison_w1.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        # 先写入column_name
        writer.writerow(["domain","ipv4", "ipv6", "ipv4_conn_time", "ipv6_conn_time", "ipv4_transfer_page_time", "ipv6_transfer_page_time","v4_v6_page_differ"])
        total = 0
        for index, r in df.iterrows():  # 遍历每一行
            domain_url = r[1]
            ipv6 = check_ipv6_deployed(domain_url)
            if (ipv6 == None):
                continue
            ipv4 = check_ipv4(domain_url)
            print("domain URL: %s, IPv4 addr: %s, IPv6 addr: %s"%(domain_url,ipv4,ipv6))
            try:
                # print("**检测网站连接速度**")
                # test_website(domain_url)
                print("**检测ipv4连接速度**")
                v4_conn_time,v4_transfer_time,v4_page_content = test_website(ipv4)
                print("**检测ipv6连接速度**")
                v6_conn_time,v6_transfer_time,v6_page_content = test_website('['+ipv6+']')
                page_differ = -1
                if(v4_page_content == v6_page_content):
                    page_differ = 0
                else:
                    page_differ = 1
                writer.writerow([domain_url, ipv4, ipv6, round(v4_conn_time, 2),round(v6_conn_time,2),round(v4_transfer_time,2),round(v6_transfer_time,2), page_differ])
                total = total + 1
                print("当前总文件行：", total)
                if(total>=10000):
                    break
            except Exception as e:
                print(e)
                continue


    # test_url = '39.156.69.79'
    # test_url = '[2606:4700:20::681a:a97]'
    # test_url = 'www.baidu.com'
    # test_website(test_url)