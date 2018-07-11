from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from .ext import db
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime, Boolean
from flask_login import UserMixin
from asset.utils import login_manager

# app = Flask(__name__)
# db = SQLAlchemy(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    """Represents Proected users."""

    # Set the name for table
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, index=True)
    password_hash = Column(String(255))
    email = Column(String(255), unique=True)
    # role_id = Column(Integer, ForeignKey('roles.id'))

    # def __init__(self, username):
    #     self.username = username
    #     self.username = username
    #     self.username = username
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute/ password 不是一个可读属性。')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    def __repr__(self):
        """Define the string format for instance of User."""
        return '<User %r>' % self.username


class Asset(db.Model):
    __tablename__ = 'Asset'

    id = Column(String(45), primary_key=True)
    type = Column(String(45), default='server')
    name = Column(String(45), unique=True)
    sn = Column(String(45), unique=True)
    buy_time = Column(DateTime)
    expire_date = Column(DateTime)
    management_ip = Column(Integer)
    # model = CharField(max_length=100, blank=True, null=True, verbose_name='资产型号')
    # put_zone = SmallIntegerField(blank=True, null=True, verbose_name='放置区域')
    business_unit = Column(String(45))
    # tags = Column('')
    # admin = ForeignKey('UserProfile', verbose_name=u'资产管理员', null=True, blank=True,on_delete=SET_NULL)
    idc = Column(String(45))

    status = Column(Integer, default='0')
    # Configuration = OneToOneField('Configuration',verbose_name='配置管理',blank=True,null=True)

    memo = Column(String(255))
    create_date = Column(DateTime)
    update_date = Column(DateTime)
    approved = Column(Boolean, default=False)


class IDC(db.Model):
    """机房"""
    __tablename__ = 'IDC'
    id = Column(String(45), primary_key=True)
    name = Column(String(64), default='阿里云')
    memo = Column(String(256))

    def __init__(self, name, memo):
        self.name = name
        self.memo = memo


class Manufactory(db.Model):
    """厂商"""
    __tablename__ = 'Manufactory'
    id = Column(String(45), primary_key=True)
    manufactory = Column(String(45))
    support_num = Column(String(30))
    memo = Column(String(256))

    def __init__(self, manufactory, memo):
        self.name = manufactory
        self.memo = memo


class BusinessUnit(db.Model):
    """业务线"""
    __tablename__ = 'BusinessUnit'
    id = Column(String(45), primary_key=True)
    name = Column(String(64), default='健康')
    memo = Column(String(256))

    def __init__(self, name, memo):
        self.name = name
        self.memo = memo
