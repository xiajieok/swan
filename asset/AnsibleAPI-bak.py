# !/usr/bin/env python

import json, datetime
import shutil
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
import ansible.constants as C
from asset.utils import get_dir

from flask import jsonify

ansible_dir = get_dir('a_path')
playbook_dir = get_dir('play_book_path')
from logger import logger as log

class PlayLogger:
    """Store log output in a single object.
    We create a new object per Ansible run
    """

    def __init__(self):
        self.log = ''
        self.runtime = 0

    def append(self, log_line):
        """append to log"""
        self.log += log_line + "\n\n"

    def banner(self, msg):
        """Output Trailing Stars"""
        width = 78 - len(msg)
        if width < 3:
            width = 3
        filler = "*" * width
        return "\n%s %s " % (msg, filler)


class ResultCallback(CallbackBase):
    def __init__(self, *args, **kwargs):
        super(ResultCallback, self).__init__(*args, **kwargs)
        self.logger = PlayLogger()
        self.start_time = datetime.datetime.now()
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}
        self.playbook_on_start = {}

        self.status_playbook = ''
        self.status_no_hosts = False

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.host_failed[result._host.get_name()] = result


class AnsibleApi(object):
    def __init__(self):
        self.Options = namedtuple('Options',
                                  ['connection',
                                   'remote_user',
                                   'ask_sudo_pass',
                                   'verbosity',
                                   'ack_pass',
                                   'module_path',
                                   'forks',
                                   'become',
                                   'become_method',
                                   'become_user',
                                   'check',
                                   'listhosts',
                                   'listtasks',
                                   'listtags',
                                   'syntax',
                                   'sudo_user',
                                   'sudo',
                                   'diff'])

        self.ops = self.Options(connection='smart',
                                remote_user='root',
                                # remote_user=None,
                                ack_pass=None,
                                sudo_user=None,
                                forks=5,
                                sudo=None,
                                ask_sudo_pass=False,
                                verbosity=5,
                                module_path=None,
                                become=None,
                                become_method=None,
                                become_user=None,
                                check=False,
                                diff=False,
                                listhosts=None,
                                listtasks=None,
                                listtags=None,
                                syntax=None)

        self.loader = DataLoader()
        self.passwords = dict()
        self.results_callback = ResultCallback()
        self.inventory = InventoryManager(loader=self.loader, sources=['/usr/local/ansible/hosts'])
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)

    def runansible(self, host_list, task_list):

        play_source = dict(
                name="Ansible Play",
                hosts=host_list,
                gather_facts='no',
                tasks=task_list
        )
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)

        tqm = None
        try:
            tqm = TaskQueueManager(
                    inventory=self.inventory,
                    variable_manager=self.variable_manager,
                    loader=self.loader,
                    options=self.ops,
                    passwords=self.passwords,
                    stdout_callback=self.results_callback,
                    run_additional_callbacks=C.DEFAULT_LOAD_CALLBACK_PLUGINS,
                    run_tree=False,
            )
            result = tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()
            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

        results_raw = {}
        results_raw['success'] = {}
        results_raw['failed'] = {}
        results_raw['unreachable'] = {}

        for host, result in self.results_callback.host_ok.items():
            # results_raw['success'][host] = json.dumps(result._result)
            results_raw['success'][host] = result._result

        for host, result in self.results_callback.host_failed.items():
            results_raw['failed'][host] = result._result['msg']

        for host, result in self.results_callback.host_unreachable.items():
            results_raw['unreachable'][host] = result._result['msg']

        log.info(results_raw)
        res = json.dumps(results_raw, indent=4)
        return res

    def playbookrun(self, playbook_path, host):
        self.variable_manager.extra_vars = {'customer': 'test', 'disabled': 'yes', 'host': host}
        playbook = PlaybookExecutor(playbooks=playbook_path,
                                    inventory=self.inventory,
                                    variable_manager=self.variable_manager,
                                    loader=self.loader, options=self.ops, passwords=self.passwords)

        result = playbook.run()

        return result


if __name__ == "__main__":
    g = AnsibleApi()
    host_list = ['master']
    # host_list = ['192.168.1.194:5000']
    # task_list = [
    #     dict(action=dict(module='shell', args='cd /root/docker  &&  docker-compose ps')),
        # dict(action=dict(module='shell', args='python sleep.py')),
        # dict(action=dict(module='synchronize', args='src=/home/op/test dest=/home/op/ delete=yes')),
    # ]

    # test = playbook_dir + 'test.yml'
    # s = a.playbookrun(playbook_path=[test],host='test')
    # print('res', s)
    cmd1 = "docker service scale  sys01_joy-api=3"

    task_list = [
        dict(action=dict(module='command', args=cmd1)),
    ]
    print(task_list)

    data = g.runansible(host_list, task_list)
    print(data)
