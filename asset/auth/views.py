from flask import render_template, redirect, request, url_for, flash, request, jsonify, g, make_response
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import User
from .forms import LoginFrom, RegistrationForm
from asset import db
from config import SECRET_KEY

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(scheme='Bearer')
multi_auth = MultiAuth(basic_auth, token_auth)

@auth.route('/set_cookie')
def set_cookie():
    token = g.user.generate_auth_token(600)
    response=make_response('Hello World')
    response.set_cookie('Authorization','True')
    response.set_cookie('token',token)
    # g.token = token
    """设置cookie"""
    # 先创建响应对象
    return response


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginFrom()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print('登录用户', user)

        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            s = set_cookie()
            print(s)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    print('NO')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    response = make_response('delete cookie')
    response.set_cookie('auth_token', '', expires=0)

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


@basic_auth.verify_password
def verify_password(username_or_token, password):
    user = User.verify_auth_token(username_or_token)
    if not user:
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@basic_auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access !!!'}), 403)


serializer = Serializer(SECRET_KEY, expires_in=600)


@token_auth.verify_token
def verify_token(token):
    g.user = None
    try:
        data = serializer.loads(token)
    except:
        return False
    if 'username' in data:
        g.user = data['username']
        return True
    return False


@token_auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access !!!'}), 403)


@auth.route('/api/token')
@multi_auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    g.token = token
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


@auth.route('/api/resource')
@multi_auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})
