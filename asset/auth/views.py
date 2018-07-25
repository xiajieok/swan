from flask import render_template, redirect, request, url_for, flash, request, jsonify, g
from flask_httpauth import HTTPTokenAuth, HTTPBasicAuth

from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import User
from .forms import LoginFrom, RegistrationForm
from asset import db

oauth = HTTPTokenAuth(scheme='Bearer')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginFrom()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print('登录用户', user)

        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    print('NO')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            user = User(email=form.email.data,
                        username=form.username.data,
                        password=form.password.data,
                        id='1')
            db.session.add(user)
            flash('You can now login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


oauth = HTTPBasicAuth()


@auth.route('/api/resource')
@oauth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})


@oauth.verify_password
def verify_password(username_or_token, password):
    user = User.verify_auth_token(username_or_token)
    if not user:
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@auth.route('/api/token')
@oauth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})
