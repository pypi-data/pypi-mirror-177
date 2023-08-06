import re

import pyhttpx
import time
import json
from pprint import pprint as pp
import time
import random
import os
import concurrent
import threading
import requests

headers={
'Connection': 'keep-alive',
'Pragma': 'no-cache',
'Cache-Control': 'no-cache',
'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
'sec-ch-ua-platform': '"Windows"',
'sec-ch-ua-mobile': '?0',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
'Content-type': 'application/x-www-form-urlencoded',
'Accept': '*/*',
'Sec-Fetch-Site': 'cross-site',
'Sec-Fetch-Mode': 'cors',
'Sec-Fetch-Dest': 'empty',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh,zh-CN;q=0.9,en;q=0.8',
}


def main():
    sess = pyhttpx.HttpSession()
    #sess = requests.session()

    d = {'Host': 'httpbin.org', 'Connection': 'keep-alive', 'Content-Length': '0',
         'Pragma': 'no-cache', 'Cache-Control': 'no-cache',
         'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
         'sec-ch-ua-platform': '"Windows"', 'sec-ch-ua-mobile': '?0',
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
         'Content-type': 'application/x-www-form-urlencoded', 'Accept': '*/*', 'Origin': 'https://www.ti.com',
         'Sec-Fetch-Site': 'cross-site', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty',
         'Referer': 'https://www.ti.com/applications/automotive/adas/overview.html',
         'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh,zh-CN;q=0.9,en;q=0.8'}

    url='https://httpbin.org/post'
    proxies = {'https': '127.0.0.1:8888'}
    r = sess.post(url, headers=d, proxies=proxies, data='123')
    print(r.text)
if __name__ == '__main__':
    main()























