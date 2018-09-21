import configparser as cf
import os
from flask import request, make_response, jsonify
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


def get_dir(args):
    dirs = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config = cf.RawConfigParser()
    with open(dirs + '/cmdb.ini', 'r') as cfgfile:
        config.read_file(cfgfile)
        a_path = config.get('config', 'ansible_path')
        # print(a_path)
        play_book_path = config.get('config', 'playbook_path')
        # print(play_book_path)
        hosts_path = config.get('config', 'hosts_path')
        swarm_path = config.get('config', 'swarm_path')
        swarm_dest_path = config.get('config', 'swarm_dest_path')
    if args:
        return vars()[args]
    else:
        return 'NO'


def get_salt(args):
    dirs = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config = cf.RawConfigParser()
    with open(dirs + '/cmdb.ini', 'r') as cfgfile:
        config.read_file(cfgfile)
        username = config.get('salt', 'username')
        password = config.get('salt', 'password')
        url = config.get('salt', 'url')
        dir = config.get('salt', 'dir')
    if args:
        return vars()[args]
    else:
        return 'NO'
