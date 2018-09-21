s = {'ruleName': 'Memory alert', 'state': 'alerting',
     'ruleUrl': 'http://localhost:3000/dashboard/db/cadvisor?fullscreen&edit&tab=alert&panelId=1',
     'title': '[Alerting] Memory alert', 'evalMatches': [
        {'metric': 'Memory {host: manager, container: sys01_api.2.kzkr1zbonjnna8g8yuw9sthj0}', 'tags': None,
         'value': 3546.9109075770193},
        {'metric': 'Memory {host: manager, container: sys01_joy-api.1.74malzjtspgoaxd54qrfsv44k}', 'tags': None,
         'value': 1186.8509575353871}], 'ruleId': 7}

# s = {'state': 'alerting', 'evalMatches': [
#     {'metric': 'Memory {host: manager, container: sys01_web.1.r86invdaz9to8nwnkfdu6eomq}', 'value': 4367437.08994004,
#      'tags': None}], 'ruleUrl': 'http://localhost:3000/dashboard/db/cadvisor?fullscreen&edit&tab=alert&panelId=1',
#      'title': '[Alerting] Memory alert', 'ruleId': 7, 'ruleName': 'Memory alert'}
# n = s['evalMatches']
#
# ss = n[0]['metric']
# old_value = n[0]['value']
# print(old_value)
#
#
# data = ss.replace('Memory '," ").replace('{host: '," ").replace('container: ',"").strip()[:-1].split()
#
# host = data[0][:-1]
# print(host)
# container = data[1]
# print(container)
# svc_name = container.split('.')[0]
# print(svc_name)
#
# threshold_value  = 2000000
# if old_value>threshold_value:
#     print('Add new mechine')
