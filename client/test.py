s1 = {'host': '192.168.1.106', 'type': 'docker-compose', 'svc': {'nginx': {'state': 'Up', 'port': '0.0.0.0:82->80/tcp'},
                                                                 'tomcat': {'state': 'Up',
                                                                            'port': '0.0.0.0:81->8080/tcp'}}}
for k,v in s1.items():
    print(k,v)
svc = s1['svc']

for k,v in svc.items():
    print(k,v)
    print(v['port'])