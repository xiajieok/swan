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

ansible_dir = get_dir('a_path')
playbook_dir = get_dir('play_book_path')

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


class ServiceList(Resource):
    # decorators = [auth.login_required]


    def get(self):

        res = {}

        try:
            data = request.args.to_dict()
            for k, v in data.items():
                if k == 'type':
                    svc = models.Service.query.filter_by(type=v)
            res = {}
            for i in svc:
                res[i.id] = {'name': i.name, 'type': i.type, 'role': i.role, 'stack': i.stack,
                             'host': i.host, 'state': i.state, 'port': i.port, 'memo': i.memo,
                             'update_date': i.update_date}

            return jsonify(res)
        except:
            svc = models.Service.query.all()
            for i in svc:
                res[i.id] = {'name': i.name, 'type': i.type, 'role': i.role, 'stack': i.stack,
                             'host': i.host, 'state': i.state, 'port': i.port, 'memo': i.memo,
                             'update_date': i.update_date}
        return jsonify(res)

    def post(self):
        url = request.url
        print(url)
        json_data = request.get_json(force=True)
        host_ip = json_data['host']

        if 'ip' in url:
            logger.info(json_data)
            for sys_type in json_data.keys():
                if sys_type == 'system':
                    svc_sys = json_data['system']
                    for k, v in svc_sys.items():
                        name = k
                        state = v['state']
                        port = v['port']
                        models.Service.query.filter_by(name=name, host=host_ip).update(
                                {"state": state, "update_date": datetime.now()})
                        db.session.commit()

                else:
                    svc_compose = json_data['docker-compose']
                    for k, v in svc_compose.items():
                        name = k
                        state = v['state']
                        port = v['port']
                        print(name)
                        models.Service.query.filter_by(name=name, host=host_ip).update(
                                {"state": state, "port": port, "update_date": datetime.now()})
                        db.session.commit()
            db.session.close()
        else:
            logger.info(json_data)
            host = json_data['host']
            svc_sys = json_data['system']
            for k, v in svc_sys.items():
                name = k
                state = v['state']
                port = v['port']
                sys = models.Service(name=name, host=host, state=state, type='system',
                                     port=port, update_date=datetime.now())
                db.session.add(sys)
                db.session.commit()

            svc_compose = json_data['docker-compose']
            for k, v in svc_compose.items():
                name = k
                state = v['state']
                port = v['port']
                print(name, state, port)
                compose = models.Service(name=name, host=host, state=state, type='docker-compose',
                                         port=port, update_date=datetime.now())
                db.session.add(compose)
                db.session.commit()
            db.session.close()
        return 200


class Service(Resource):
    # decorators = [auth.login_required]

    def get(self, service_id):
        svc = models.Service.query.filter_by(id=service_id).first()
        res = {}
        for i in svc:
            res[i.id] = {'name': i.name, 'host': i.host, 'state': i.state, 'port': i.port, 'type': i.type,
                         'memo': i.memo,
                         'update_date': i.update_date}
        return jsonify(res)

    def delete(self, service_id):
        try:
            idc = models.Service.query.filter_by(id=service_id).delete()
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
        print('id', id)

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
        elif json_data['type'] == 'cmd':

            if 'ip' in json_data.keys():

                desc = models.Asset.query.filter_by(ip=json_data['ip']).first()
                host = desc.hostname
                logger.info('docker 执行操作')

            else:
                host = json_data['hostname']
                logger.info('一般shell操作')

            # host_list = []
            task_list = [
                dict(action=dict(module='shell', args=json_data['args'])),
                # dict(action=dict(module='synchronize', args='src=/home/op/test dest=/home/op/ delete=yes')),
            ]
            # host_list.append(host)
            # logger.info(host_list)

            res = g.runansible(host, task_list)
            logger.info(res)
            ss = json.loads(res)
            if 'ip' in json_data.keys():
                logger.info(json_data['ip'])
                msg = jsonify(ss['success'][json_data['ip']]['stdout'])
                # msg = jsonify(ss['success'][json_data['ip']]['stdout'])
                logger.info(msg)
            else:
                res = models.Asset.query.filter_by(hostname=json_data['hostname']).first()
                logger.info(res.ip)
                msg = jsonify(ss['success'][res.ip]['stdout'])
                # msg = jsonify(ss['success'][json_data['ip']]['stdout'])
                logger.info(msg)
            return msg
        else:
            host = 'venv'
            tasks_list = [
                dict(action=dict(module='shell', args=json_data['cmd'])),
            ]

            res = g.runansible(host, tasks_list)
            res_dict = json.loads(res)['success'][host]['stdout']
            tmp = res_dict.split('\n')
            all = {}
            msg_dict = {}

            for i in tmp:
                line = i.split()
                # print(line)
                if len(line) > 1:
                    svc_name = line[0][7:-2]
                    state = line[-2]
                    port = line[-1]
                    if len(svc_name) > 1:
                        msg_dict[svc_name] = {}
                        msg_dict[svc_name]['port'] = port
                        msg_dict[svc_name]['state'] = state
                        all.update(msg_dict)
                        # return jsonify(all)
