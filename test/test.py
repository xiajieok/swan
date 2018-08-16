import json

s1 = {"docker-compose": {"nginx01": {"port": "0.0.0.0:30001->80/tcp", "state": "Up"},
                         "tomcat01": {"port": "0.0.0.0:30002->8080/tcp", "state": "Up"}},
      "system": {"mysqld": {"port": "null", "state": "STOP"}, "nginx": {"port": "null", "state": "RUN"},
                 "docker": {"port": "null", "state": "STOP"}, "sshd": {"port": "null", "state": "RUN"}}}





docker = s1['docker-compose']
system = s1['system']

for type in s1.keys():
    if type == 'system':
        svc_sys = s1['system']
        for k,v in svc_sys.items():
            name = k
            state = v['state']
            port = v['port']
            print(name,state,port)
    else:
        svc_compose = s1['docker-compose']
        for k,v in svc_compose.items():
            name = k
            state = v['state']
            port = v['port']
            print(name,state,port)