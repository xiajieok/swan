from flask import request
from flask_login import LoginManager
from flask_httpauth import HTTPTokenAuth

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


auth = HTTPTokenAuth(scheme='Bearer')


@auth.verify_token
def get_password(username):
    data = request.cookies
    print(data)
    res = request.cookies.get('Authorization')
    print('res',res)
    return res

