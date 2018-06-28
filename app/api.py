from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,jsonify
)
from werkzeug.exceptions import abort

# from flaskr.auth import login_required
from app.db import get_db


bp = Blueprint('api', __name__)

@app.route("/api/server")
def server():
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from  cow_server")
    data = cursor.fetchall()
    if data is None:
        return jsonify({'error': 'Not found'}, 404)
    else:
        return jsonify(data)
