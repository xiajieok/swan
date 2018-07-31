from flask import request,make_response,jsonify
from flask_login import LoginManager
from flask_httpauth import HTTPTokenAuth

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


auth = HTTPTokenAuth(scheme='Bearer')


@auth.verify_token
def get_password(username):
    res = request.cookies.get('Authorization')
    return res
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access !!!'}), 403)


