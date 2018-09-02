from flask import Blueprint
from flask_restful import Api
from asset.api import views

restful_api = Blueprint('restful_api', __name__, url_prefix='/api')
resource = Api(restful_api)

# resource.add_resource(views.Token,"/token")
resource.add_resource(views.User, "/user/<int:user_id>")
resource.add_resource(views.UserList, "/user")
resource.add_resource(views.IDCList, "/idc")
resource.add_resource(views.IDC, "/idc/<int:idc_id>")

#service
resource.add_resource(views.ServiceList, "/service")
resource.add_resource(views.Service, "/service")

resource.add_resource(views.BusinessUnitList, "/business")
resource.add_resource(views.BusinessUnit, "/business/<int:business_id>")
resource.add_resource(views.AssetList, "/assets")
resource.add_resource(views.Asset, "/assets/<int:asset_id>")

# ansible
resource.add_resource(views.Ansible, "/ansible")

# Dashboard
resource.add_resource(views.Dashboard, "/dashboard_data")

# domain
resource.add_resource(views.DomainList, "/domain")
resource.add_resource(views.Domain, "/domain/<int:domain_id>")

# vpn
resource.add_resource(views.VpnList, "/vpn")
resource.add_resource(views.Vpn, "/vpn/<int:vpn_id>")
