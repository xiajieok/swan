import json, os

s1 = {'192.168.1.106': {'type': 'docker-compose', 'name': {'nginx': {'state': 'Up', 'port': '0.0.0.0:82->80/tcp'},
                                                           'tomcat': {'state': 'Up', 'port': '0.0.0.0:81->8080/tcp'}}}}
# host = s1.keys()
# for i in host:
#
#     name = s1[i]['name']
#     print(name)
#     # state = s1[i]['name']['state']
#     for k, v in name.items():
#         print(k, v)
#         name = k
#         print(name)



#
# for k,v in ss.items():
#     print(k,v)














#
#
# s1 = {"dev": {"nginx": {"state": "Up", "port": "0.0.0.0:82->80/tcp"},
#               "tomcat": {"state": "Up", "port": "0.0.0.0:81->8080/tcp"}}}
#
# s2 = {"dev": {"name": {"nginx": {"state": "Up", "port": "0.0.0.0:82->80/tcp"}},
#               "tomcat": {"state": "Up", "port": "0.0.0.0:81->8080/tcp"}}}
#
ss = {'type': 'docker-compose', 'host': 'dev', 'svc': {'nginx': {'state': 'Up', 'port': '0.0.0.0:82->80/tcp'},
                                                       'tomcat': {'state': 'Up', 'port': '0.0.0.0:81->8080/tcp'}}}
def get_svc():
    cmd = 'cd /opt/docker && docker-compose ps'
    res = os.popen(cmd).read().split('\n')
    all = {}
    msg_dict = {}
    msg_dict['host'] = 'dev'
    msg_dict['host']['type'] = 'docker-compose'
    msg_dict['host']['svc'] = {}
    for i in res:
        line = i.split()
        # print(line)
        if len(line) > 1:
            svc_name = line[0][7:-2]
            state = line[-2]
            port = line[-1]
            if len(svc_name) > 1:
                msg_dict['host']['svc'][svc_name] = {}
                msg_dict['host']['svc'][svc_name]['port'] = port
                msg_dict['host']['svc'][svc_name]['state'] = state
                all.update(msg_dict)
    return json.dumps(all)


print((get_svc()))
