import os
from flask_restful import reqparse, abort, Api, Resource
from flask_moment import datetime
from asset import models
from flask import jsonify, request, render_template
from asset.ext import db
from asset.utils import auth
from asset.AnsibleAPI import AnsibleApi
from asset.utils import get_dir
import json
from asset.main.dashboard import AssetDashboard
from logger import logger
import yaml
from sqlalchemy.sql import exists

ansible_dir = get_dir('a_path')
playbook_dir = get_dir('play_book_path')
swarm_dir = get_dir('swarm_path')

parser = reqparse.RequestParser()


class Dashboard(Resource):
    def get(self):
        dashboard_data = AssetDashboard(request)
        return jsonify(dashboard_data.searilize_page())


class UserList(Resource):
    decorators = [auth.login_required]

    def get(self):
        user = models.User.query.all()
        res = {}
        for i in user:
            res[i.id] = {'username': i.username, 'email': i.email}
        return jsonify(res)

    def post(self):
        json_data = request.get_json(force=True)

        res = models.User(username=json_data['username'], email=json_data['email'],
                          password=json_data['password'])
        db.session.add(res)
        db.session.commit()
        db.session.close()
        return json_data, 200


class User(Resource):
    decorators = [auth.login_required]

    def get(self, user_id):
        user = models.User.query.filter_by(id=user_id)
        res = {}
        for i in user:
            res[i.id] = {'username': i.username, 'email': i.email}
        return jsonify(res)

    def put(self, user_id):
        json_data = request.get_json(force=True)
        for i in json_data:
            models.User.query.filter_by(id=user_id).update({i: json_data[i]})
        db.session.commit()
        db.session.close()
        return 200

    def delete(self, user_id):
        try:
            user = models.User.query.filter_by(id=user_id).delete()
            db.session.commit()
            db.session.close()
        except:
            return "Not exists"
        return 200


class DomainList(Resource):
    # decorators = [auth.login_required]

    def get(self):
        domain = models.Domain.query.all()
        res = {}
        for i in domain:
            res[i.id] = {'name': i.name, 'url': i.url, 'ip': i.ip, 'memo': i.memo}
        return jsonify(res)

    def post(self):
        json_data = request.get_json(force=True)
        res = models.Domain(name=json_data['name'], url=json_data['url'], ip=json_data['ip'], memo=json_data['memo'])
        db.session.add(res)
        db.session.commit()
        db.session.close()
        return json_data, 200


class Domain(Resource):
    # decorators = [auth.login_required]

    def get(self, domain_id):
        domain = models.Domain.query.filter_by(id=domain_id)
        res = {}
        for i in domain:
            res[i.id] = {'name': i.name, 'url': i.url, 'ip': i.ip, 'memo': i.memo}
        return jsonify(res)

    def put(self, domain_id):
        json_data = request.get_json(force=True)
        for i in json_data:
            models.Domain.query.filter_by(id=domain_id).update({i: json_data[i]})
        db.session.commit()
        db.session.close()
        return 200

    def delete(self, domain_id):
        try:
            idc = models.Domain.query.filter_by(id=domain_id).delete()
            print(idc)
            db.session.commit()
            db.session.close()
        except:
            return "Not exists"
        return 200


class VpnList(Resource):
    # decorators = [auth.login_required]

    def get(self):
        vpn = models.Vpn.query.all()
        res = {}
        for i in vpn:
            res[i.id] = {'name': i.name, 'create_date': i.create_date, 'memo': i.memo}
        return jsonify(res)

    def post(self):
        json_data = request.get_json(force=True)
        res = models.Vpn(name=json_data['name'], create_date=datetime.now(), memo=json_data['memo'])
        db.session.add(res)
        db.session.commit()
        db.session.close()
        return json_data, 200


class Vpn(Resource):
    # decorators = [auth.login_required]

    def get(self, vpn_id):
        vpn = models.Vpn.query.filter_by(id=vpn_id)
        res = {}
        for i in vpn:
            res[i.id] = {'name': i.name, 'create_date': i.create_date, 'memo': i.memo}
        return jsonify(res)

    def put(self, vpn_id):
        json_data = request.get_json(force=True)
        for i in json_data:
            models.Vpn.query.filter_by(id=vpn_id).update({i: json_data[i]})
        db.session.commit()
        db.session.close()
        return 200

    def delete(self, vpn_id):
        try:
            idc = models.Vpn.query.filter_by(id=vpn_id).delete()
            print(idc)
            db.session.commit()
            db.session.close()
        except:
            return "Not exists"
        return 200


class IDCList(Resource):
    decorators = [auth.login_required]

    def get(self):
        idc = models.IDC.query.all()
        res = {}
        for i in idc:
            res[i.id] = {'name': i.name, 'memo': i.memo}
        return jsonify(res)

    def post(self):
        json_data = request.get_json(force=True)
        res = models.IDC(name=json_data['name'], memo=json_data['memo'])
        db.session.add(res)
        db.session.commit()
        db.session.close()
        return json_data, 200


class IDC(Resource):
    decorators = [auth.login_required]

    def get(self, idc_id):
        idc = models.IDC.query.filter_by(id=idc_id)
        res = {}
        for i in idc:
            res[i.id] = {'name': i.name, 'memo': i.memo}
        return jsonify(res)

    def put(self, idc_id):
        json_data = request.get_json(force=True)
        for i in json_data:
            models.IDC.query.filter_by(id=idc_id).update({i: json_data[i]})
        db.session.commit()
        db.session.close()
        return 200

    def delete(self, idc_id):
        try:
            idc = models.IDC.query.filter_by(id=idc_id).delete()
            print(idc)
            db.session.commit()
            db.session.close()
        except:
            return "Not exists"
        return 200


class BusinessUnitList(Resource):
    decorators = [auth.login_required]

    def get(self):
        business = models.BusinessUnit.query.all()
        res = {}
        for i in business:
            res[i.id] = {'name': i.name, 'memo': i.memo}
        return jsonify(res)

    def post(self):
        json_data = request.get_json(force=True)
        res = models.BusinessUnit(name=json_data['name'], memo=json_data['memo'])
        db.session.add(res)
        db.session.commit()
        db.session.close()
        return json_data, 200


class BusinessUnit(Resource):
    decorators = [auth.login_required]

    def get(self, business_id):
        business = models.BusinessUnit.query.filter_by(id=business_id)
        res = {}
        for i in business:
            res[i.id] = {'name': i.name, 'memo': i.memo}
        return jsonify(res)

    def put(self, business_id):
        json_data = request.get_json(force=True)
        for i in json_data:
            models.BusinessUnit.query.filter_by(id=business_id).update({i: json_data[i]})
        db.session.commit()
        db.session.close()
        return 200

    def delete(self, business_id):
        try:
            idc = models.BusinessUnit.query.filter_by(id=business_id).delete()
            print(idc)
            db.session.commit()
            db.session.close()
        except:
            return "Not exists"
        return 200


class YamlList(Resource):
    def get(self):
        res = {}

        svc = models.Yaml.query.all()
        for i in svc:
            res[i.id] = {'name': i.svc_name, 'stack': i.stack, 'image': i.image, 'networks': i.networks,
                         'volumes': i.volumes,
                         'replicas': i.replicas, 'constraints': i.constraints, 'cpus': i.cpus, 'memory': i.memory,
                         'state': i.state, 'ports': i.ports, 'memo': i.memo,
                         'update_date': datetime.now()}
        return jsonify(res)

    def post(self):
        json_data = request.get_json(force=True)
        if db.session.query(exists().where(models.Yaml.svc_name == json_data['svc_name'])).scalar() is not True:
            res = models.Yaml(stack=json_data['stack'], svc_name=json_data['svc_name'], image=json_data['image'],
                              ports=json_data['ports'], networks=json_data['networks'], volumes=json_data['volumes'],
                              replicas=json_data['replicas'], constraints=json_data['constraints'], cpus=json_data['cpus'],
                              memory=json_data['memory'], update_date=datetime.now())

            db.session.add(res)
            db.session.commit()
            db.session.close()
            # node = '[node.role == manager]'
            swarm_file = get_dir('swarm_path') + json_data['svc_name'] + '.yml'
            data = {
                'version': '3.0',
                'services': {
                    json_data['svc_name']: {
                        'image': json_data['image'],
                        'ports': [json_data['ports']],
                        'networks': [json_data['networks']],
                        'volumes': [json_data['volumes']],
                        'deploy': {
                            'mode': 'replicated',
                            'replicas': int(json_data['replicas']),
                            'placement': {
                                'constraints': [json_data['constraints']]
                            },
                            'resources': {
                                'limits': {
                                    'cpus': json_data['cpus'],
                                    'memory': json_data['memory']
                                }

                            }
                        }
                    }
                },
                'networks': {
                    json_data['networks']:
                        {'driver': 'overlay'}
                },

            }
            print(data)
            f = open(swarm_file, 'w')
            yaml.dump(data, f,default_flow_style=False,indent=2,encoding='utf-8',allow_unicode=True)
            f.close()

            # 传输swarm文件
            g = AnsibleApi()
            src_file = swarm_file

            cmd = 'src=' + src_file + ' backup=yes dest=' + swarm_dir
            task_list = [
                dict(action=dict(module='copy', args=cmd)),
                # dict(action=dict(module='synchronize', args='src=/home/op/test dest=/home/op/ delete=yes')),
            ]
            print(task_list)
            res = g.runansible('localhost.localdomain', task_list)
            print(res)
        else:
            json_data ='NO'

        return json_data, 200


class ServiceList(Resource):
    # decorators = [auth.login_required]

    def get(self):
        res = {}

        svc = models.Service.query.all()
        for i in svc:
            res[i.id] = {'name': i.svc_name, 'stack': i.stack, 'image': i.image, 'networks': i.networks,
                         'volumes': i.volumes,
                         'replicas': i.replicas, 'constraints': i.constraints, 'cpus': i.cpus, 'memory': i.memory,
                         'state': i.state, 'ports': i.ports, 'memo': i.memo,
                         'update_date': i.update_date}
        return jsonify(res)

    def post(self):
        json_data = request.get_json(force=True)
        json_data = json.loads(json_data)
        ss = {}
        for k, v in json_data.items():
            svc_name = k
            for svc in v.items():
                if svc[0] == 'deploy':
                    deploy = svc[1]
                    print(deploy)
                    ss['replicas'] = deploy['replicas']
                    ss['mode'] = deploy['mode']
                    ss['constraints'] = deploy['placement']['constraints']
                    ss['cpus'] = deploy['resources']['limits']['cpus']
                    ss['memory'] = deploy['resources']['limits']['memory']
                    pass
                else:
                    ss[svc[0]] = svc[1]
            if '192.168.1.232' in ss['image']:
                ss['image'] = ss['image'][19:]

            else:
                ss['image'] = ss['image']
            try:
                ss['volumes'] = ",".join(ss['volumes'])
            except:
                ss['volumes'] = 'Null'
            res = models.Service(svc_name=svc_name, stack='APP', image=ss['image'], ports=ss['ports'][0],
                                 networks=ss['networks'][0],
                                 replicas=ss['replicas'], constraints=ss['constraints'][0][5:], cpus=ss['cpus'],
                                 memory=ss['memory'], volumes=ss['volumes'],
                                 state=ss['state'], update_date=datetime.now())
            db.session.add(res)
            db.session.commit()
            db.session.close()
            # print(res)
        return 200


class Service(Resource):
    # decorators = [auth.login_required]

    def get(self, service_id):
        svc = models.Service.query.filter_by(id=service_id).first()
        res = {}
        res[svc.id] = {'name': svc.svc_name, 'stack': svc.stack, 'image': svc.image, 'networks': svc.networks,
                       'volumes': svc.volumes,
                       'replicas': svc.replicas, 'constraints': svc.constraints, 'cpus': svc.cpus, 'memory': svc.memory,
                       'state': svc.state, 'ports': svc.ports, 'memo': svc.memo,
                       'update_date': svc.update_date}
        return jsonify(res)

    def put(self):
        json_data = request.get_json(force=True)
        json_data = json.loads(json_data)
        ss = {}
        for k, v in json_data.items():
            svc_name = k
            for svc in v.items():
                if svc[0] == 'deploy':
                    deploy = svc[1]
                    ss['replicas'] = deploy['replicas']
                    ss['mode'] = deploy['mode']
                    ss['constraints'] = deploy['placement']['constraints']
                    ss['cpus'] = deploy['resources']['limits']['cpus']
                    ss['memory'] = deploy['resources']['limits']['memory']
                    pass
                else:
                    ss[svc[0]] = svc[1]
            print(ss)

            if '192.168.1.232' in ss['image']:
                ss['image'] = ss['image'][19:]
            else:
                ss['image'] = ss['image']
            logger.info(ss)
            try:
                ss['volumes'] = ",".join(ss['volumes'])
            except:
                ss['volumes'] = 'Null'

            res = models.Service.query.filter_by(svc_name=svc_name).update(
                {'image': ss['image'], 'ports': ss['ports'][0],
                 'networks': ss['networks'][0],
                 'replicas': ss['replicas'], 'constraints': ss['constraints'][0][5:], 'cpus': ss['cpus'],
                 'memory': ss['memory'], 'volumes': ss['volumes'],
                 'state': ss['state'], 'update_date': datetime.now()})

            db.session.commit()
            db.session.close()
            # print(res)
        return 200

    def delete(self, service_id):
        try:
            svc = models.Service.query.filter_by(id=service_id).delete()
            db.session.commit()
            db.session.close()
        except:
            return "Not exists"
        return 200


class AssetList(Resource):
    # decorators = [auth.login_required]

    def get(self):
        # print(request.args)

        try:
            data = request.args.to_dict()
            for k, v in data.items():
                if k == 'idc':
                    asset = models.Asset.query.filter_by(idc=v)
                elif k == 'business_unit':
                    asset = models.Asset.query.filter_by(business_unit=v)
                else:
                    asset = models.Asset.query.filter_by(type=v)
            res = {}
            for i in asset:
                res[i.id] = {'hostname': i.hostname, 'type': i.type, 'sn': i.sn, 'ip': i.ip,
                             'model': i.model, "cpu_processor": i.cpu_processor, "cpu_model": i.cpu_model,
                             "cpu_num": i.cpu_num, "vendor": i.vendor, "os": i.os,
                             "cpu_physical": i.cpu_physical, "disk": i.disk, "memory": i.memory,
                             'status': i.status, 'idc': i.idc, 'business_unit': i.business_unit,
                             'expire_date': i.expire_date, 'create_date': i.create_date,
                             'update_date': i.update_date,
                             'approved': i.approved, 'memo': i.memo}

            return jsonify(res)
        except:
            asset = models.Asset.query.all()
            res = {}
            for i in asset:
                res[i.id] = {'hostname': i.hostname, 'type': i.type, 'sn': i.sn, 'ip': i.ip,
                             'model': i.model, "cpu_processor": i.cpu_processor, "cpu_model": i.cpu_model,
                             "cpu_num": i.cpu_num, "vendor": i.vendor, "os": i.os,
                             "cpu_physical": i.cpu_physical, "disk": i.disk, "memory": i.memory,
                             'status': i.status, 'idc': i.idc, 'business_unit': i.business_unit,
                             'expire_date': i.expire_date, 'create_date': i.create_date,
                             'update_date': i.update_date,
                             'approved': i.approved, 'memo': i.memo}

            return jsonify(res)

    def post(self):
        json_data = request.get_json(force=True)
        logger.info(json_data)
        res = models.Asset(hostname=json_data['hostname'], ip=json_data['ip'], sn=json_data['sn'],
                           type=json_data['type'],
                           os=json_data['os'], vendor=json_data['vendor'],
                           model=json_data['model'], cpu_processor=json_data['cpu_processor'],
                           cpu_model=json_data['cpu_model'],
                           cpu_num=json_data['cpu_num'], cpu_physical=json_data['cpu_physical'],
                           memory=json_data['memory'], disk=json_data['disk'],
                           idc=json_data['idc'], create_date=datetime.now(), update_date=datetime.now(),
                           status=json_data['status'])
        db.session.add(res)
        db.session.commit()
        db.session.close()
        res = db.session.query(models.Asset).filter_by(ip=json_data['ip']).first()
        id = res.id
        db.session.close()
        # update hosts
        host_file = get_dir('hosts_path')
        with open(host_file, 'a+') as f:
            f.write('\n' + '[' + json_data['hostname'] + ']' + '\n')
            f.write(json_data['ip'])

        return id


class Asset(Resource):
    # decorators = [auth.login_required]

    def get(self, asset_id):
        asset = models.Asset.query.filter_by(id=asset_id).first()
        res = {}
        res[asset.id] = {'hostname': asset.hostname, 'type': asset.type, 'sn': asset.sn, 'model': asset.model,
                         'ip': asset.ip, "cpu_processor": asset.cpu_processor, "cpu_model": asset.cpu_model,
                         "cpu_num": asset.cpu_num, "os": asset.os, "vendor": asset.vendor,
                         "cpu_physical": asset.cpu_physical, "disk": asset.disk, "memory": asset.memory,
                         'status': asset.status, 'idc': asset.idc, 'business_unit': asset.business_unit,
                         'expire_date': asset.expire_date, 'create_date': asset.create_date,
                         'update_date': asset.update_date,
                         'approved': asset.approved, 'memo': asset.memo}

        return jsonify(res)

    def put(self, asset_id):
        json_data = request.get_json(force=True)
        logger.info(json_data)
        logger.info(json_data)
        for i in json_data:
            models.Asset.query.filter_by(id=asset_id).update({i: json_data[i], "update_date": datetime.now()})
        db.session.commit()
        db.session.close()
        return 200

    def delete(self, asset_id):
        try:
            asset = models.Asset.query.filter_by(id=asset_id).delete()
            print(asset)
            db.session.commit()
            db.session.close()
        except:
            return "Not exists"
        return 200


class Ansible(Resource):
    def get(self):
        # 获取yaml文件
        playbook_dir = get_dir('play_book_path')
        list = os.listdir(playbook_dir)
        books = {}
        for i in list:
            name = i[:-4]
            value = i
            books[name] = value
        return jsonify(books)

    def post(self):

        # 根据获取到 主机名/playbook 执行操作
        json_data = request.get_json(force=True)
        logger.info(json_data)
        g = AnsibleApi()
        if json_data['type'] == 'playbook':
            test = playbook_dir + 'test.yml'
            try:
                callback = g.playbookrun(playbook_path=[test], host=json_data['hostname'])
                if callback == 0:
                    return 'Successful !!!'
            except:
                return "Faild !!!"
        else:

            if 'ip' in json_data.keys():

                desc = models.Asset.query.filter_by(ip=json_data['ip']).first()
                host = desc.hostname
                logger.info('docker 执行操作')

            else:
                host = json_data['hostname']
                logger.info('一般shell操作')
                print('一般shell操作')

            task_list = [
                dict(action=dict(module='raw', args=json_data['args'])),
                # dict(action=dict(module='synchronize', args='src=/home/op/test dest=/home/op/ delete=yes')),
            ]
            print(task_list)
            res = g.runansible(host, task_list)
            print(res)
            logger.info(res)
            ss = json.loads(res)
            try:
                if 'ip' in json_data.keys():
                    logger.info(json_data['ip'])
                    msg = jsonify(ss['success'][json_data['ip']]['stdout'])
                    # msg = jsonify(ss['success'][json_data['ip']]['stdout'])
                    logger.info(msg)
                else:
                    res = models.Asset.query.filter_by(hostname=host).first()
                    print(res)
                    logger.info(res.ip)
                    msg = jsonify(ss['success'][res.ip]['stdout'])

                    # msg = jsonify(ss['success'][json_data['ip']]['stdout'])
                    logger.info(msg)
                return msg
            except:
                return 'Error'
