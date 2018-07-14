from flask_restful import reqparse, abort, Api, Resource
from flask_moment import datetime
from asset import models
from flask import jsonify, request
from asset.ext import db

parser = reqparse.RequestParser()


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
        print('new_id',new_id)
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
        idc = models.BusinessUnit.query.all()
        res = {}
        for i in idc:
            res[i.id] = {'name': i.name, 'memo': i.memo}
        return jsonify(res)

    def post(self):
        json_data = request.get_json(force=True)
        try:
            idc_id = models.BusinessUnit.query.order_by(models.IDC.id.desc()).first().id
            new_id = int(idc_id) + 1
        except:
            new_id = 1
        print(new_id)
        res = models.BusinessUnit(id=new_id, name=json_data['name'], memo=json_data['memo'])
        db.session.add(res)
        db.session.commit()
        db.session.close()
        return json_data, 200


class BusinessUnit(Resource):
    def get(self):
        idc = models.BusinessUnit.query.all()
        res = {}
        for i in idc:
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
            idc = models.BusinessUnit.query.filter_by(id=idc_id).delete()
            print(idc)
            db.session.commit()
            db.session.close()
        except:
            return "Not exists"
        return 200


class AssetList(Resource):
    def get(self):
        # print(request.args)

        try:
            data = request.args.to_dict()
            for k,v in data.items():
                if k == 'idc':
                    asset = models.Asset.query.filter_by(idc=v)
                elif k == 'business_unit':
                    asset = models.Asset.query.filter_by(business_unit=v)
                else:
                    asset = models.Asset.query.filter_by(type=v)
            res = {}
            for i in asset:
                res[i.id] = {'name': i.name, 'type': i.type, 'sn': i.sn, 'management_ip': i.management_ip,
                             'status': i.status, 'idc': i.idc, 'business_unit': i.business_unit,
                             'expire_date': i.expire_date, 'create_date': i.create_date,
                             'update_date': i.update_date,
                             'approved': i.approved, 'memo': i.memo}

            return jsonify(res)
        except:
            asset = models.Asset.query.all()
            res = {}
            for i in asset:
                res[i.id] = {'name': i.name, 'type': i.type, 'sn': i.sn, 'management_ip': i.management_ip,
                             'status': i.status, 'idc': i.idc, 'business_unit': i.business_unit,
                             'expire_date': i.expire_date, 'create_date': i.create_date,
                             'update_date': i.update_date,
                             'approved': i.approved, 'memo': i.memo}

            return jsonify(res)

    def post(self):
        json_data = request.get_json(force=True)
        print('提交到的数据',json_data)
        try:
            asset_id = models.Asset.query.order_by(models.Asset.id.desc()).first().id
            new_id = int(asset_id) + 1
        except:
            new_id = 1
        res = models.Asset(id=new_id, name=json_data['name'], sn=json_data['sn'], type=json_data['type'],
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
        res[asset.id] = {'name': asset.name, 'type': asset.type, 'sn': asset.sn, 'management_ip': asset.management_ip,
                         'status': asset.status, 'idc': asset.idc, 'business_unit': asset.business_unit,
                         'expire_date': asset.expire_date, 'create_date': asset.create_date,
                         'update_date': asset.update_date,
                         'approved': asset.approved, 'memo': asset.memo}

        return jsonify(res)

    def put(self, asset_id):
        json_data = request.get_json(force=True)
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
