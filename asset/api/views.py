from flask_restful import reqparse, abort, Api, Resource
from flask_moment import datetime
from asset import models
from flask import jsonify, request
from asset.ext import db

parser = reqparse.RequestParser()


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class User(Resource):
    def get(self):
        user = models.User.query.all()
        res = {}
        for i in user:
            res[i.id] = {'username': i.username, 'email': i.email}
        return jsonify(res)


class IDC(Resource):
    def get(self):
        user = models.IDC.query.all()
        res = {}
        for i in user:
            res[i.id] = {'name': i.name, 'memo': i.memo}
        return jsonify(res)


class AssetList(Resource):
    def get(self):
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
        print(request.method)
        json_data = request.get_json(force=True)
        asset_id = models.Asset.query.order_by(models.Asset.id.desc()).first().id
        new_id = int(asset_id) + 1
        res = models.Asset(id=new_id, name=json_data['name'], sn=json_data['sn'], type=json_data['type'],
                           idc=json_data['idc'], create_date=datetime.now(), status=json_data['status'])
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
        asset = models.Asset.query.filter_by(id=asset_id).first()
        for i in json_data:
            print(i)
            # asset.i = json_data[i]
            models.Asset.query.filter_by(id=asset_id).update(i=json_data[i])
        # asset.status = json_data['status']
        # # db.session.add(asset)
        args = parser.parse_args()
        db.session.commit()
        db.session.close()
        return 200
