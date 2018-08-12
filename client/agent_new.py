#!/usr/bin/env python
# coding=utf-8
import os, re, platform, socket, time, json, threading
import psutil, dmidecode
import requests
from subprocess import Popen, PIPE
import fcntl
import struct
import logging

AGENT_VERSION = "1.0"
token = 'HPcWR7l4NJNJ'
server_ip = '192.168.47.130'


def get_ip():
    '''
    #mac
    try:
        hostname = socket.getfqdn(socket.gethostname())
        ipaddr = socket.gethostbyname(hostname)
    except Exception as msg:
        print(msg)
        ipaddr = ''
    return ipaddr
    '''
    '''
    linux
    '''
    ifname = 'eth0'
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
    )[20:24])


def get_dmi():
    p = Popen('dmidecode', stdout=PIPE, shell=True)
    stdout, stderr = p.communicate()
    return stdout


def parser_dmi(dmidata):
    pd = {}
    line_in = False
    for line in dmidata.split('\n'):
        if line.startswith('System Information'):
            line_in = True
            continue
        if line.startswith('\t') and line_in:
            k, v = [i.strip() for i in line.split(':')]
            pd[k] = v
        else:
            line_in = False
    return pd


def get_mem_total():
    cmd = "grep MemTotal /proc/meminfo"
    p = Popen(cmd, stdout=PIPE, shell=True)
    data = p.communicate()[0]
    mem_total = data.split()[1]
    memtotal = int(round(int(mem_total) / 1024.0 / 1024.0, 0))
    return memtotal


def get_cpu_model():
    cmd = "cat /proc/cpuinfo"
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = p.communicate()
    return stdout


def get_cpu_cores():
    cmd = 'cat /proc/cpuinfo| grep "physical id"| sort| uniq| wc -l'
    num = os.popen(cmd).read().replace("\n", "")
    cpu_cores = {"physical": psutil.cpu_count(logical=False) if psutil.cpu_count(logical=False) else 0,
                 "logical": psutil.cpu_count(), "num": num}
    print('cpu_cores', cpu_cores)
    return cpu_cores


def get_svc():
    cmd = 'cd /opt/docker && docker-compose ps'
    res = os.popen(cmd).read().split('\n')
    all = {}
    ip = get_ip()
    msg_dict = {}
    msg_dict['host'] = ip
    msg_dict['type'] = 'docker-compose'
    msg_dict['svc'] = {}
    for i in res:
        line = i.split()
        # print(line)
        if len(line) > 1:
            svc_name = line[0][7:-2]
            state = line[-2]
            port = line[-1]
            if len(svc_name) > 1:
                msg_dict['svc'][svc_name] = {}
                msg_dict['svc'][svc_name]['port'] = port
                msg_dict['svc'][svc_name]['state'] = state
                all.update(msg_dict)
    # print(all)
    return json.dumps(all)


def parser_cpu(stdout):
    groups = [i for i in stdout.split('\n\n')]
    group = groups[-2]
    cpu_list = [i for i in group.split('\n')]
    cpu_info = {}
    for x in cpu_list:
        k, v = [i.strip() for i in x.split(':')]
        cpu_info[k] = v
    return cpu_info


def get_disk_info():
    ret = []
    cmd = "fdisk -l|egrep '^Disk\s/dev/[a-z]+:\s\w*'"
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = p.communicate()
    for i in stdout.split('\n'):
        disk_info = i.split(",")
        if disk_info[0]:
            ret.append(disk_info[0])
    return ret


def post_data(url, data):
    try:
        r = requests.post(url, data)
    # if r.text:
    #     logging.info(r.text)
    # else:
    #     logging.info("Server return http status code: {0}".format(r.status_code))
    except Exception as msg:
        print(msg)
    # logging.info(msg)
    return True


def machine_info():
    # info = dmidecode.profile()
    # info_keys = info.keys()
    # for i in range(len(info_keys)):
    #     if info[info_keys[i]]['dmi_type'] == 1:
    #         Product_name = info[info_keys[i]]['data']['Product Name']
    #         return Product_name
    return 'Dell'


def asset_info():
    data_info = dict()
    data_info['idc'] = 'beijing'
    data_info['type'] = 'server'
    data_info['status'] = 'RUN'
    data_info['memory'] = str(get_sys_mem())
    # data_info['memory'] = get_mem_total()
    data_info['disk'] = str(get_disk_info())

    cpuinfo = parser_cpu(get_cpu_model())
    cpucore = get_cpu_cores()
    data_info['cpu_num'] = cpucore['num']
    data_info['cpu_processor'] = cpucore['logical']
    data_info['cpu_physical'] = cpucore['physical']
    data_info['cpu_model'] = cpuinfo['model name']

    data_info['ip'] = get_ip()
    data_info['sn'] = parser_dmi(get_dmi())['Serial Number']
    data_info['vendor'] = parser_dmi(get_dmi())['Manufacturer']
    # data_info['model'] = parser_dmi(get_dmi())['Version']
    data_info['model'] = machine_info()
    data_info['os'] = platform.linux_distribution()[0] + " " + platform.linux_distribution()[
        1] + " " + platform.machine()
    data_info['hostname'] = platform.node()
    # data_info['token'] = token
    # data_info['agent_version'] = AGENT_VERSION
    print(data_info)
    return json.dumps(data_info)


# def new_asset_info():
#     data = {
#
#         # "vendor": "QEMU",
#         "type": "server",
#         "model": "Dell",
#         "status": "stop",
#         "ip": "192.168.1.3",
#         "hostname": "vultr.1.gs1t",
#         "cpu_model": "Virtual CPU a7769a6388d5",
#         "cpu_physical": 2,
#         "cpu_processor": 4,
#         "cpu_num": 210,
#         # "product": "pc-i440fx-2.10",
#         # "token": "HPcWR7l4NJNJ",
#         # "osver": "CentOS Linux 7.3.1611 x86_64",
#         "sn": "ASDKJANSKDASJ",
#         "idc": "Beijing",
#         "memory": 10,
#         "disk": "[]",
#         # "agent_version": "1.0"
#     }
#     return data

# def asset_info_post(status,id):
#     print(status,id)
#     # pversion = platform.python_version()
#     # pv = re.search(r'2.6', pversion)
#     # if not pv:
#     # 	osenv = os.environ["LANG"]
#     # 	os.environ["LANG"] = "us_EN.UTF8"
#     # logging.info('Get the hardwave infos from host:')
#     # logging.info(asset_info())
#     print('----------------------------------------------------------')
#     if status == "new":
#         # print(new_asset_info())
#         url = "http://scm.joy.com/api/assets"
#         data = new_asset_info()
#         data['id'] = id
#         print(data)
#
#         res = requests.post(url, json.dumps(data))
#         print(res)
#         # if not pv:
#         # 	os.environ["LANG"] = osenv
#         return True
#     else:
#         url = "http://scm.joy.com/api/assets/" + str(id)
#         res = requests.put(url, json.dumps(new_asset_info()))
#         print(res)
#         # if not pv:
#         # 	os.environ["LANG"] = osenv
#         return True

def get_sys_cpu():
    sys_cpu = {}
    cpu_time = psutil.cpu_times_percent(interval=1)
    sys_cpu['percent'] = psutil.cpu_percent(interval=1)
    sys_cpu['lcpu_percent'] = psutil.cpu_percent(interval=1, percpu=True)
    sys_cpu['user'] = cpu_time.user
    sys_cpu['nice'] = cpu_time.nice
    sys_cpu['system'] = cpu_time.system
    sys_cpu['idle'] = cpu_time.idle
    sys_cpu['iowait'] = cpu_time.iowait
    sys_cpu['irq'] = cpu_time.irq
    sys_cpu['softirq'] = cpu_time.softirq
    sys_cpu['guest'] = cpu_time.guest
    return sys_cpu


def get_sys_mem():
    sys_mem = {}
    mem = psutil.virtual_memory()
    sys_mem["total"] = int(mem.total / 1024 / 1024 / 1024)
    sys_mem["percent"] = mem.percent
    sys_mem["available"] = int(mem.available / 1024 / 1024 / 1024)
    sys_mem["used"] = int(mem.used / 1024 / 1024 / 1024)
    sys_mem["free"] = int(mem.free / 1024 / 1024 / 1024)
    sys_mem["buffers"] = int(mem.buffers / 1024 / 1024 / 1024)
    sys_mem["cached"] = int(mem.cached / 1024 / 1024 / 1024)
    return sys_mem


def parser_sys_disk(mountpoint):
    partitions_list = {}
    d = psutil.disk_usage(mountpoint)
    partitions_list['mountpoint'] = mountpoint
    partitions_list['total'] = round(d.total / 1024 / 1024 / 1024.0, 2)
    partitions_list['free'] = round(d.free / 1024 / 1024 / 1024.0, 2)
    partitions_list['used'] = round(d.used / 1024 / 1024 / 1024.0, 2)
    partitions_list['percent'] = d.percent
    return partitions_list


def get_sys_disk():
    sys_disk = {}
    partition_info = []
    partitions = psutil.disk_partitions()
    for p in partitions:
        partition_info.append(parser_sys_disk(p.mountpoint))
    sys_disk = partition_info
    return sys_disk


# 函数获取各网卡发送、接收字节数
def get_nic():
    key_info = psutil.net_io_counters(pernic=True).keys()  # 获取网卡名称

    recv = {}
    sent = {}

    for key in key_info:
        recv.setdefault(key, psutil.net_io_counters(pernic=True).get(key).bytes_recv)  # 各网卡接收的字节数
        sent.setdefault(key, psutil.net_io_counters(pernic=True).get(key).bytes_sent)  # 各网卡发送的字节数

    return key_info, recv, sent


# 函数计算每秒速率
def get_nic_rate(func):
    key_info, old_recv, old_sent = func()  # 上一秒收集的数据
    time.sleep(1)
    key_info, now_recv, now_sent = func()  # 当前所收集的数据

    net_in = {}
    net_out = {}

    for key in key_info:
        net_in.setdefault(key, (now_recv.get(key) - old_recv.get(key)) / 1024)  # 每秒接收速率
        net_out.setdefault(key, (now_sent.get(key) - old_sent.get(key)) / 1024)  # 每秒发送速率

    return key_info, net_in, net_out


def get_net_info():
    net_info = []
    key_info, net_in, net_out = get_nic_rate(get_nic)
    for key in key_info:
        in_data = net_in.get(key)
        out_data = net_out.get(key)
        net_info.append({"nic_name": key, "traffic_in": in_data, "traffic_out": out_data})
    return net_info


def info_post():
    # 判断是否存在pid文件
    if os.path.isfile('.id'):
        with open('.id', 'r') as f:
            id = f.read()
        # return 'old',id
        url = "http://scm.joy.com/api/assets/" + str(id)

        data = json.loads(asset_info())
        data.pop('sn')
        data.pop('hostname')
        res = requests.put(url, json.dumps(data))
        print('update  sys')


        url2 = "http://scm.joy.com/api/service" + str(get_ip())
        data = json.loads(get_svc())
        data['host'] = get_ip()
        print(data)
        res = requests.put(url2, json.dumps(data))
        print('update svc')
        # if not pv:
        # 	os.environ["LANG"] = osenv
        return True
    else:
        url = "http://scm.joy.com/api/assets"
        res = requests.get(url).text
        id_list = json.loads(res)
        # print(type(msg),msg.keys())
        if len(id_list) < 1:
            id = 1
        else:
            id = int(max(id_list)) + 1
        print('This is new id', id)
        with open('.id', 'w') as f:
            f.write(str(id))
        data = json.loads(asset_info())
        data['id'] = id
        print(data)

        res = requests.post(url, json.dumps(data))


        url2 = "http://scm.joy.com/api/service"
        data = json.loads(get_svc())
        data['host'] = get_ip()
        res = requests.post(url2, json.dumps(data))
        # if not pv:
        # 	os.environ["LANG"] = osenv
        return res.text


def post_svc():
    url2 = "http://scm.joy.com/api/service"
    data = json.loads(get_svc())
    data['host'] = get_ip()
    res = requests.post(url2, json.dumps(data))
    print(res)


if __name__ == "__main__":
    msg = info_post()
    print(msg)
    # res = post_svc()
    # print(res)
