from flask import render_template
from sqlalchemy import func
from app.main import app
import app.models as models


def idc_data():
    data = models.db.session.query(models.IDC).order_by(id).all()
    return data


@app.route('/')
@app.route('/idc')
def idc():
    data = models.db.session.query(models.IDC).order_by(id).all()
    return render_template('idc.html',idc=idc)
