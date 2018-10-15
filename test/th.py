#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:medivh
@file: falcon.py
@time: 2018/10/14
"""

import json
import time
import threading
from time import ctime, sleep
import requests

test_joy = {
    'CALCULATOR-API': 'https://www.baidu.com',
    'CALCULATOR-SVC': 'http://192.168.1.221:8061/health',
    'CONSULT-API': 'http://192.168.1.221:8087/health',
    'CONSULT-SVC': 'http://192.168.1.221:8088/health'
}
joy = {
    'CONSUMER-SERVICE (683a6d92)': 'http://192.168.28.8:11111/health',
    'CALCULATOR-API (efbdf744)': 'http://192.168.80.4:11131/health',
    'CALCULATOR-API (cb36ea30)': 'http://192.168.12.2:11040/health',
    'CALCULATOR-SERVICE (ec3e97d5)': 'http://192.168.12.3:11050/health',
    'CALCULATOR-SERVICE (f7a3bc67)': 'http://192.168.28.4:11051/health',
    'CONSULT-API (ef267291)': 'http://192.168.28.5:11061/health',
    'CONSULT-API (a0b2d7ea)': 'http://192.168.12.7:11060/health',
    'CONSULT-SERVICE (10b82ace)': 'http://192.168.28.6:11071/health',
    'CONSULT-SERVICE (ccbf7361)': 'http://192.168.12.4:11070/health',
    'CONSUMER-API (2e3f6368)': 'http://192.168.28.2:11110/health',
    'CONSUMER-API (476e7121)': 'http://192.168.12.5:11110/health',
    'CONSUMER-API (baf400eb)': 'http://192.168.85.8:11110/health',
    'CONSUMER-API (a25e5113)': 'http://192.168.78.9:11110/health',
    'DATA-SYNC (c760f029)': 'http://192.168.28.7:11123/health',
    'DP-POOL-SERVICE (dc8804a8)': 'http://192.168.25.2:11130/health',
    'DP-POOL-SERVICE (537dc7bd)': 'http://192.168.107.2:11130/health',
    'EPAY-API (072a2845)': 'http://192.168.78.3:11081/health',
    'EPAY-API (006a8ff5)': 'http://192.168.85.2:11081/health',
    'EPAY-BANK (a076286b)': 'http://192.168.78.2:11080/health',
    'EPAY-BANK (7cda355f)': 'http://192.168.85.4:11080/health',
    'EPAY-SERVICE (7b36822f)': 'http://192.168.85.3:11082/health',
    'EPAY-SERVICE (6a6a0524)': 'http://192.168.78.4:11082/health',
    'EPAY-TIMER (fccad940)': 'http://192.168.78.5:11083/health',
    'JOY-ADMIN-SERVER (7771c8e0)': 'http://192.168.100.4:17777/health',
    'JOY-HYSTRIX-TURBINE (ec807eba)': 'http://192.168.100.5:17766/health',
    'JOYAPI-GATEWAY (f4695f77)': 'http://192.168.2.6:10051/health',
    'JOYAPI-GATEWAY (3ba2752c)': 'http://192.168.100.7:10050/health',
    'JOYSHEBAO-GATEWAY (e15f6809)': 'http://192.168.100.9:10010/health',
    'JOYSHEBAO-GATEWAY (401cf28e)': 'http://192.168.100.8:10010/health',
    'JOYSHEBAO-GATEWAY (ece0f625)': 'http://192.168.2.3:10010/health',
    'JOYSHEBAO-GATEWAY (214b4323)': 'http://192.168.2.2:10010/health',
    'MARKET (ffe62112)': 'http://192.168.80.2:11140/health',
    'MARKET (8a63586d)': 'http://192.168.95.2:11140/health',
    'NOTICE-SERVICE (5da0cb9c)': 'http://192.168.85.5:11030/health',
    'NOTICE-SERVICE (01b139e0)': 'http://192.168.78.6:11030/health',
    'SEARCH-SERVICE (e7b7b11e)': 'http://192.168.28.10:11124/health',
    'WECHAT (c0583f46)': 'http://192.168.85.6:11090/health',
    'WECHAT (1f0210a8)': 'http://192.168.78.7:11090/health'
}

count = 5

payload_data = []
payload_status = []


def check_url(svc_name, svc_url):
    t = []
    res_code = 'UP'
    for i in range(count):
        try:
            r = requests.get(svc_url, timeout=3)
            res_code = r.json()['status']
            res_time = r.elapsed.microseconds / 1000
            t.append(res_time)
            sleep(1)
        except Exception as e:
            print('%s is Down or Timeout!!!' % svc_name)
            res_code = 'DOWN'
    avg_time = sum(t) / count
    ts = int(time.time())

    svc_data = {
        "endpoint": "Service",
        "metric": svc_name,
        "timestamp": ts,
        "step": 60,
        "value": avg_time,
        "counterType": "GAUGE",
        "tags": svc_name

    }
    payload_data.append(svc_data)

    if res_code == 'UP':
        status = '1'
    else:
        status = '0'

    svc_status = {
        "endpoint": "Service",
        "metric": svc_name + '.alive',
        "timestamp": ts,
        "step": 60,
        "value": status,
        "counterType": "GAUGE",
        "tags": svc_name

    }
    payload_status.append(svc_status)


def push_open_falcon():
    r_status = requests.post("http://127.0.0.1:1988/v1/push", data=json.dumps(payload_status))
    r_data = requests.post("http://127.0.0.1:1988/v1/push", data=json.dumps(payload_data))
    print(r_status)


threads = []

# 创建线程
for k, v in joy.items():
    t = threading.Thread(target=check_url, args=(k, v))
    threads.append(t)

if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()
    # push to open-falcon
    push_open_falcon()
    print("all over %s" % ctime())
