from flask_sqlalchemy import SQLAlchemy
from app import main

db = SQLAlchemy(main.app)

class IDC(db.Model):
    """机房"""
    __tablename__ = 'IDC'
    id = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(64),default='阿里云')
    memo = db.Column(db.String(256))

    def __init__(self,name):
        self.name = name

