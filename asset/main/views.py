import os
from datetime import datetime
from flask import Flask
from flask import render_template, session, redirect, url_for
from flask_login import login_required
from .forms import IDCFrom
from . import main


@main.route('/')
@login_required
def index():
    return render_template('index.html')


@main.route('/asset')
@login_required
def asset():
    return render_template('asset.html')


@main.route('/asset/add')
@login_required
def asset_add():
    return render_template('asset_add.html')


@main.route('/idc')
@login_required
def idc():
    return render_template('idc.html')


@main.route('/app')
@login_required
def app():
    return render_template('app.html')
@main.route('/domain')
@login_required
def domain():
    return render_template('domain.html')


@main.route('/ansible')
@login_required
def ansible():
    return render_template('ansible.html')

@main.route('/salt')
@login_required
def salt():
    return render_template('salt.html')

@main.route('/swarm')
@login_required
def swarm():
    return render_template('swarm.html')

@main.route('/swarm_edit')
@login_required
def swarm_edit():
    return render_template('swarm_add.html')

@main.route('/other')
@login_required
def other():
    return render_template('other.html')


@main.route('/services')
@login_required
def services():
    return render_template('services.html')


@main.route('/user')
@login_required
def user():
    return render_template('user.html')


@main.route('/secret')
def secret():
    return 'Only authenticated users ar allowed!'
