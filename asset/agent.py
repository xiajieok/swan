#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18/8/8 18:52
# @Author  : Medivh


from asset.AnsibleAPI import MyRunner
# 传入inventory路径
ansible = MyRunner('/usr/local/ansible/hosts')
# 获取服务器磁盘信息
ansible.run('all', 'setup', "filter='ansible_mounts'")
#结果
result=ansible.get_result()
print(result)
#成功
succ = result['success']
print(succ)
#失败
failed = result['failed']
#不可到达
unreachable = result['unreachable']

