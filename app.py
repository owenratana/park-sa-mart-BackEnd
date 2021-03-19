from flask import Flask, request, jsonify, session, url_for, redirect, flash
from flask_mysqldb import MySQL
import yaml
import pymysql
from functools import wraps
import jwt
import datetime



app = Flask(__name__)
db = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_PORT'] = db['mysql_port']
app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = 'parksamart'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

import user
import auth
import parkman

# def check_token(func):
#     @wraps(func)
#     def wrapped(*args, **kwargs):
#         token = request.args.get('token')
#         if not token:
#             return jsonify({'message' : 'Missing token'}), 403
#         try:
#             data = jwt.decode(token, app.config['SECRET_KEY'], 'HS256')
#         except:
#             return jsonify({'message' : 'Invalid token'}), 403
#         return func(*args, **kwargs)
#     return wrapped

def check_token(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            token = request.json['token']
            try:
                data = jwt.decode(token, app.config['SECRET_KEY'], 'HS256')
            except:
                return jsonify({'message' : 'Invalid token'}), 403
        except:
            return jsonify({'message' : 'Missing token'}), 403
        
        return func(*args, **kwargs)
    return wrapped

@app.route('/register', methods=['POST'])
def register():
    return auth.register()

@app.route('/login', methods=['POST'])
def login():
    return auth.login()

@app.route('/home', methods=['GET', 'POST'])
@check_token
def home():
    token = request.json['token']
    email = jwt.decode(token, app.config['SECRET_KEY'], 'HS256')['email']
    return email + ' you have valid token'


@app.route('/addcar', methods=['POST'])
@check_token
def addcar():
    return user.addcar()


@app.route('/editprofile', methods=['POST'])
@check_token
def editprofile():
    return user.editprofile()

@app.route('/addcard', methods=['POST'])
@check_token
def addcard():
    return user.addcard()



if __name__ == '__main__' :     
    app.run(debug=True, host = '0.0.0.0')
