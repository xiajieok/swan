from flask import Flask, g
from .ext import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime, Boolean
from flask_login import UserMixin
from asset.utils import login_manager
from config import SECRET_KEY
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    """Represents Proected users."""

    # Set the name for table
    __tablename__ = 'user'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True, index=True)
    password_hash = Column(String(255))
    email = Column(String(255), unique=True)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute/ password 不是一个可读属性。')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
        # user = User.query.filter_by(username = username).first()
        # if not user or not user.verify_password(password):
        #     return False
        # g.user = user
        # return True

    def generate_auth_token(self, expiration=600):
        s = Serializer(SECRET_KEY, expires_in=expiration)
        data = s.dumps({'id': self.id})
        print(data)
        return data

    @staticmethod
    def verify_auth_token(token, expiration=600):
        s = Serializer(SECRET_KEY, expires_in=expiration)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user


class Asset(db.Model):
    __tablename__ = 'Asset'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    type = Column(String(64), default='server')
    hostname = Column(String(64), unique=True)
    sn = Column(String(64), unique=True)
    buy_time = Column(DateTime)
    expire_date = Column(DateTime)
    ip = Column(String(128))
    disk = Column(String(128))
    model = Column(String(64))
    # 内存相关
    memory = Column(String(256))
    # CPU相关
    cpu_model = Column(String(128))
    # 逻辑核数
    cpu_processor = Column(String(32))
    # 数量
    cpu_num = Column(String(32))
    # 核
    cpu_physical = Column(String(32))
    business_unit = Column(String(64))
    # 厂商型号
    vendor = Column(String(64))
    os = Column(String(128))

    # tags = Column('')
    # admin = ForeignKey('UserProfile', verbose_name=u'资产管理员', null=True, blank=True,on_delete=SET_NULL)
    idc = Column(String(64))

    status = Column(String(64), default='running')
    # Configuration = OneToOneField('Configuration',verbose_name='配置管理',blank=True,null=True)

    memo = Column(String(255))
    create_date = Column(DateTime)
    update_date = Column(DateTime)
    approved = Column(Boolean, default=False)


class Service(db.Model):
    """服务"""
    __tablename__ = 'Service'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(64))
    type = Column(String(64))
    role = Column(String(64))
    stack = Column(String(64))
    host = Column(String(64))
    state = Column(String(64))
    port = Column(String(256))
    update_date = Column(DateTime)
    memo = Column(String(256))


class IDC(db.Model):
    """机房"""
    __tablename__ = 'IDC'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(64), default='阿里云')
    create_date = Column(DateTime)
    memo = Column(String(256))


class Domain(db.Model):
    """域名"""
    __tablename__ = 'Domain'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(64))
    url = Column(String(64))
    ip = Column(String(64))
    memo = Column(String(256))


# def __init__(self, name, memo):
#     self.name = name
#     self.memo = memo


class Manufactory(db.Model):
    """厂商"""
    __tablename__ = 'Manufactory'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    manufactory = Column(String(64))
    support_num = Column(String(32))
    memo = Column(String(256))


# def __init__(self, manufactory, memo):
#     self.name = manufactory
#     self.memo = memo


class BusinessUnit(db.Model):
    """业务线"""
    __tablename__ = 'BusinessUnit'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(64), default='健康')
    memo = Column(String(256))

# def __init__(self, name, memo):
#     self.name = name
#     self.memo = memo
