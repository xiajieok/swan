# coding:utf-8
import json
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase


class ResultCallback(CallbackBase):
    def v2_runner_on_ok(self, result, **kwargs):
        host = result._host
        print(json.dumps({host.name: result._result}, indent=4))


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
        self.results_callback = ResultCallback()

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

        # 开始执行
        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options,
                passwords=self.passwords,
                stdout_callback=self.results_callback,  # 使用自定义回调代替“default”回调插件（如不需要stdout_callback参数则按照默认的方式输出）
            )
            result = tqm.run(play)
            print(result)
        finally:
            if tqm is not None:
                tqm.cleanup()


if __name__ == "__main__":
    g = AnsibleApi()
    host_list = ['scm']
    cmd1 = "/usr/bin/python /root/new_file.py"
    task_list = [
        dict(action=dict(module='shell', args=cmd1),register='shell_out'),
    ]
    print(task_list)

    data = g.runansible(host_list, task_list)
