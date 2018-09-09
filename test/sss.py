import os

# cmd = "ocker service ps " + 'sys01_joy-api' + "  |grep Running"
# svc_node_res = os.popen(cmd).read().split('\n')
# print(svc_node_res)
# for i in svc_node_res:
#     print(svc_node_res)

s = [
    'lm5toys1xpi3  sys01_joy-api.1      docker.io/nginx:latest  localhost.localdomain  Running        Running about an hour ago                                     ',
    'rwn2jwxnq9cj  sys01_joy-api.2      docker.io/nginx:latest  localhost.localdomain  Running        Running 17 minutes ago                                        ',
    '']
print(str(s))
# nodes = []
# for i in s:
#     # print(i)
#     if len(i) > 0:
#         node = i.split()[3]
#         nodes.append(node)
# print(nodes)