#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:medivh
@file: SaltAPI.py
@time: 2018/09/21
"""

import urllib, ssl, json,re
from urllib import parse, request


class SaltAPI(object):
    # init attribute
    def __init__(self, url, username, password):
        self.__url = url.rstrip('/')
        self.__user = username
        self.__password = password
        self.__token_id = self.salt_login()
        self.__context = ssl._create_unverified_context()
        self.__headers = {'X-Auth-Token': ''}
        self.__params = {'client':'local'}
    def salt_login(self):
        params = {'eauth': 'pam', 'username': self.__user, 'password': self.__password}
        data = urllib.parse.urlencode(params).encode('utf-8')
        headers = {'X-Auth-Token': ''}
        context = ssl._create_unverified_context()
        url = self.__url + '/login'

        data = request.Request(url=url, headers=headers, data=data)
        # SSL
        # context = ssl._create_unverified_context()
        res = request.urlopen(data, context=context).read().decode()
        try:
            token = json.loads(res)['return'][0]['token']
        except KeyError:
            raise KeyError
        return token
    def postRequest(self,obj,prefix='/'):
        headers = {'X-Auth-Token': self.__token_id}
        data = obj.encode('utf-8')
        url = self.__url
        context = ssl._create_unverified_context()
        req = request.Request(url=url, headers=headers, data=data)
        res = request.urlopen(req, context=context).read()
        return res

    def salt_fun(self,params):
        obj = urllib.parse.urlencode(params).encode('utf-8')
        print(obj)
        obj = obj.decode()
        obj,number = re.subn("arg\d",'arg',obj)
        print(obj,number)
        try:
            res = self.postRequest(obj).decode()
            res = json.loads(res)
            return res

        except urllib.request.HTTPError as e:
            raise e
    def cmd(self,tgt,arg):
        self.__params['tgt'] = tgt
        self.__params['fun'] = 'cmd.run'
        self.__params['arg'] = arg
        try:
            res = self.salt_fun(self.__params)
            return res
        except urllib.request.HTTPError as e:
            raise e

if __name__ == '__main__':
    salt = SaltAPI(url='https://192.168.1.232:8888', username='saltapi', password='salt')
    test = salt.salt_login()
    # params = {'client':'local', 'fun':'cmd.run', 'tgt':'*','arg':'free -m'}
    tgt = 'scm'
    arg = 'df -h'

    test = salt.cmd(tgt,arg)['return'][0]
    print(test)
