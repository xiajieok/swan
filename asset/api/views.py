from datetime import datetime
from flask_restful import Resource,Api
import asset.models as models

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}
class UserInfo(Resource):
    def get(self):
        user = models.User.query.all()
        print(user)
        return user