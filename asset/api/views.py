import os
from flask_restful import reqparse, abort, Api, Resource
from flask_moment import datetime
from asset import models
from flask import jsonify, request, render_template
from asset.ext import db
from asset.utils import auth
from asset.utils import get_dir
# from asset.AnsibleAPI import AnsibleApi
from asset.utils import get_dir
import json
from asset.main.dashboard import AssetDashboard

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
            res[i.id] = {'name': i.name,'url': i.url, 'ip': i.ip,'memo': i.memo}
        return jsonify(res)

    def post(self):
        json_data = request.get_json(force=True)
        res = models.Domain(name=json_data['name'],url=json_data['url'],ip=json_data['ip'], memo=json_data['memo'])
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
            res[i.id] =  {'name': i.name,'url': i.url, 'ip': i.ip,'memo': i.memo}
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
        svc = models.Service.query.all()
        res = {}
        for i in svc:
            res[i.id] = {'name': i.name, 'type': i.type, 'role': i.role, 'stack': i.stack,
                         'host': i.host, 'state': i.state, 'port': i.port, 'memo': i.memo,
                         'update_date': i.update_date}
        return jsonify(res)

    def post(self):
        json_data = request.get_json(force=True)
        # print(json_data)
        host = json_data['host']
        type = json_data['type']
        svc = json_data['svc']
        for k, v in svc.items():
            name = k
            port = v['port']
            state = v['state']
            res = models.Service(name=k, host=host, state=state, type=type,
                                 port=port)
            db.session.add(res)
            db.session.commit()
        db.session.close()
        return json_data, 200


class Service(Resource):
    # decorators = [auth.login_required]

    def get(self, service_id):
        idc = models.Service.query.filter_by(id=service_id)
        res = {}
        for i in idc:
            res[i.id] = {'name': i.name, 'host': i.host, 'state': i.state, 'port': i.port, 'memo': i.memo}
        return jsonify(res)

    def put(self, host):
        json_data = request.get_json(force=True)
        print(json_data)
        type = json_data['type']
        svc = json_data['svc']
        for k, v in svc.items():
            name = k
            port = v['port']
            state = v['state']
            print(port, state)
            models.Service.query.filter_by(host=host, name=name).update(port=port, state=state)
            db.session.commit()
        db.session.close()
        return 200

    def delete(self, service_id):
        try:
            idc = models.Service.query.filter_by(id=service_id).delete()
            self.x = print(idc)
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
        print('提交到的数据', json_data)

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
        return json_data, 200


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
        print('更新操作')
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
    pass
    # def get(self):
    #     # 获取yaml文件
    #     playbook_dir = get_dir('play_book_path')
    #     list = os.listdir(playbook_dir)
    #     books = {}
    #     for i in list:
    #         name = i[:-4]
    #         value = i
    #         books[name] = value
    #     return jsonify(books)
    #
    # def post(self):
    #     # 根据获取到 主机名/playbook 执行操作
    #     json_data = request.get_json(force=True)
    #     print('提交到的数据', json_data)
    #     print()
    #     try:
    #         desc = models.Asset.query.filter_by(hostname=json_data['hostname']).first()
    #     except:
    #         desc.ip = 'all'
    #     print(desc.ip)
    #     g = AnsibleApi()
    #     if json_data['type'] == 'playbook':
    #         test = playbook_dir + 'test.yml'
    #         try:
    #             callback = g.playbookrun(playbook_path=[test], host=json_data['hostname'])
    #             if callback == 0:
    #                 return 'Successful !!!'
    #         except:
    #             return "Faild !!!"
    #     elif json_data['type'] == 'cmd':
    #
    #         tasks_list = [
    #             dict(action=dict(module='shell', args=json_data['cmd'])),
    #             # dict(action=dict(module='synchronize', args='src=/home/op/test dest=/home/op/ delete=yes')),
    #         ]
    #         res = g.runansible(desc.ip, tasks_list)
    #         ss = json.loads(res)
    #         try:
    #             msg = jsonify(ss['success'][desc.ip]['stdout'])
    #             # print('成功返回',msg)
    #         except:
    #             msg = jsonify(ss['failed'][desc.ip])
    #         # res = ansible.runansible(desc.ip, tasks_list)['success'][desc.ip]
    #         # res = jsonify(s)
    #         # res = json.dumps(s,indent=4)
    #         return msg
    #     else:
    #
    #         tasks_list = [
    #             dict(action=dict(module='shell', args=json_data['cmd'])),
    #         ]
    #
    #         res = g.runansible(desc.ip, tasks_list)
    #         res_dict = json.loads(res)['success'][desc.ip]['stdout']
    #         tmp = res_dict.split('\n')
    #         all = {}
    #         msg_dict = {}
    #
    #         for i in tmp:
    #             line = i.split()
    #             # print(line)
    #             if len(line) > 1:
    #                 svc_name = line[0][7:-2]
    #                 state = line[-2]
    #                 port = line[-1]
    #                 if len(svc_name) > 1:
    #                     msg_dict[svc_name] = {}
    #                     msg_dict[svc_name]['port'] = port
    #                     msg_dict[svc_name]['state'] = state
    #                     all.update(msg_dict)
    #         # return jsonify(all)
