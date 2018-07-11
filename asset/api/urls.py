from flask import Blueprint
from flask_restful import Api
from asset.api import views
restful_api = Blueprint('restful_api', __name__,url_prefix='/api')
resource = Api(restful_api)
resource.add_resource(views.HelloWorld,"/hello")
resource.add_resource(views.User,"/UserInfo")
resource.add_resource(views.IDC,"/idc")
resource.add_resource(views.AssetList,"/assets")
resource.add_resource(views.Asset,"/assets/<int:asset_id>")

