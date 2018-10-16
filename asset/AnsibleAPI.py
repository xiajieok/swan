# !/usr/bin/env python

import json
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase


class ModelResultsCollector(CallbackBase):
    def __init__(self, *args, **kwargs):
        super(ModelResultsCollector, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result):
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result):
        self.host_failed[result._host.get_name()] = result


class AnsibleApi(object):
    # 初始化需要的对象
    def __init__(self):
        self.Options = namedtuple('Options',
                                  ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user',
                                   'check',
                                   'diff'])

        # module_path参数指定本地ansible模块包的路径
        self.loader = DataLoader()
        self.options = self.Options(connection='smart',
                                    module_path='/Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/site-packages/ansible/modules',
                                    forks=5, become=None, become_method=None, become_user="root", check=False,
                                    diff=False)
        self.passwords = dict(vault_pass='secret')

        # 实例化ResultCallback来处理结果
        # self.results_callback = ModelResultsCollector()

        # 创建库存(inventory)并传递给VariableManager
        self.inventory = InventoryManager(loader=self.loader,
                                          sources=['/usr/local/ansible/hosts'])  # ../conf/hosts是定义hosts
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)

    def runansible(self, host_list, task_list):
        # 创建任务
        play_source = dict(
            name="Ansible Play",
            hosts=host_list,
            gather_facts='no',
            remote_user='root',
            tasks=task_list
        )
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)
        callback = ModelResultsCollector()

        # 开始执行
        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options,
                passwords=self.passwords,
                stdout_callback=callback,
                # stdout_callback=self.results_callback,  # 使用自定义回调代替“default”回调插件（如不需要stdout_callback参数则按照默认的方式输出）
            )
            result = tqm.run(play)
            result_raw = {'success': {}, 'failed': {}, 'unreachable': {}}
            for host, result in callback.host_ok.items():
                result_raw['success'][host] = result._result
            for host, result in callback.host_failed.items():
                result_raw['failed'][host] = result._result

            msg = json.dumps(result_raw, indent=4)
            return msg

        finally:
            if tqm is not None:
                tqm.cleanup()
        # return self.results_callback

    def playbookrun(self, playbook_path, host):
        self.variable_manager.extra_vars = {'customer': 'test', 'disabled': 'yes', 'host': host}
        playbook = PlaybookExecutor(playbooks=playbook_path,
                                    inventory=self.inventory,
                                    variable_manager=self.variable_manager,
                                    loader=self.loader, passwords=self.passwords)

        result = playbook.run()
        return result


if __name__ == "__main__":
    g = AnsibleApi()
    host_list = ['scm']
    cmd1 = "/usr/bin/python /root/new_file.py"
    # cmd1 = "uname -a"
    task_list = [
        dict(action=dict(module='shell', args=cmd1), register='shell_out'),
    ]
    print(task_list)

    data = g.runansible(host_list, task_list)
