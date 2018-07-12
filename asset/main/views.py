from datetime import datetime
from flask import Flask
from flask import render_template,session,redirect,url_for
from flask_login import login_required
from . import main


@main.route('/')
@login_required
def index():
    return render_template('index.html')

@main.route('/asset')
def asset():
    return render_template('asset.html')

@main.route('/asset/add')
def asset_add():
    return render_template('asset_add.html')
@main.route('/secret')
def secret():
    return 'Only authenticated users ar allowed!'

