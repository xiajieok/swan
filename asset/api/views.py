from flask_restful import reqparse, abort, Api, Resource
from flask_httpauth import HTTPTokenAuth

from flask_moment import datetime
from asset import models
from flask import jsonify, request, g
from asset.ext import db

parser = reqparse.RequestParser()

auth = HTTPTokenAuth(scheme='Bearer')


class UserList(Resource):
    def get(self):
        user = models.User.query.all()
        res = {}
        for i in user:
            res[i.id] = {'username': i.username, 'email': i.email}
        return jsonify(res)

    def post(self):
        json_data = request.get_json(force=True)
        try:
            id = models.User.query.order_by(models.User.id.desc()).first().id
            new_id = int(id) + 1
        except:
            new_id = 1
        print('new_id', new_id)
        res = models.User(id=new_id, username=json_data['username'], email=json_data['email'],
                          password=json_data['password'])
        db.session.add(res)
        db.session.commit()
        db.session.close()
        return json_data, 200


class User(Resource):
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
        try:
            idc_id = models.IDC.query.order_by(models.IDC.id.desc()).first().id
            new_id = int(idc_id) + 1
        except:
            new_id = 1
        print(new_id)
        res = models.IDC(id=new_id, name=json_data['name'], memo=json_data['memo'])
        db.session.add(res)
        db.session.commit()
        db.session.close()
        return json_data, 200


class IDC(Resource):
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
    def get(self):
        business = models.BusinessUnit.query.all()
        res = {}
        for i in business:
            res[i.id] = {'name': i.name, 'memo': i.memo}
        return jsonify(res)

    def post(self):
        json_data = request.get_json(force=True)
        try:
            business_id = models.BusinessUnit.query.order_by(models.BusinessUnit.id.desc()).first().id
            new_id = int(business_id) + 1
        except:
            new_id = 1
        print(new_id)
        res = models.BusinessUnit(id=new_id, name=json_data['name'], memo=json_data['memo'])
        db.session.add(res)
        db.session.commit()
        db.session.close()
        return json_data, 200


class BusinessUnit(Resource):
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
        try:
            asset_id = models.Asset.query.order_by(models.Asset.id.desc()).first().id
            new_id = int(asset_id) + 1
        except:
            new_id = 1
        res = models.Asset(id=new_id, hostname=json_data['hostname'], sn=json_data['sn'], type=json_data['type'],
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


