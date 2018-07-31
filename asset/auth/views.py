from flask import render_template, redirect, request, url_for, flash, request, jsonify, g, make_response
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import User
from .forms import LoginFrom, RegistrationForm
from asset import db


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginFrom()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print('登录用户', user)

        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            redirect_to_index = redirect(request.args.get('next') or url_for('main.index'))
            token = g.user.generate_auth_token(600)
            response = make_response(redirect_to_index)
            response.set_cookie('Authorization', 'True')
            response.set_cookie('token', token)
            return response
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


