import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, jsonify, make_response
# from flask import *
from contextlib import closing
from flaskext.mysql import MySQL

app = Flask(__name__)

# DEBUG = True
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'youxia'
# app.config['MYSQL_DATABASE_DB'] = 'flask'
# app.config['MYSQL_DATABASE_HOST'] = '192.168.1.174'

app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

mysql = MySQL()
mysql.init_app(app)


@app.route("/")
def hello():
    return "Welcome to Python Flask App!"




@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run()
