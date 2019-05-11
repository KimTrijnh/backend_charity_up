
from flask import Flask, redirect,render_template, url_for, flash, jsonify, request
from flask_cors import CORS
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import login_required, current_user, LoginManager

app=Flask(__name__)
CORS(app)

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
from src.models import *

@app.route('/')
@app.route('/home')
def home():
    return 'hello'

# AUTH VIEWS
def check_username(username):
    user = UserVisit.query.filter_by(username=username).first()
    if user:
        return True
    else:
        return False

def check_email(email):
    user = UserVisit.query.filter_by(email=email).first()
    if user:
        return True
    else:
        return False  

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()
        if not check_username(data['username']) and not check_email(data['email']):
            user = UserVisit(username=data['username'], email=data['email'])
            user.set_password(data['password'])
            db.session.add(user)
            db.session.commit()
            return jsonify({
                'success': True,
                'user_id': user.id,
                'username' : user.username
                })
        else:
            return jsonify({
                'success': False,
                'error': 'username or email already taken'
            })
    return jsonify({'message': 'failed'})



@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        user = UserVisit.query.filter_by(username=data['username']).first()
        if user and user.check_password(data['password']):
            return jsonify({'isLogin': True, 'current_user': user.username })
        else:
            return jsonify({'isLogin': False, 'message': 'Wrong Username/Password'})
    return redirect("http://localhost:3000/login")
    

# @app.route('/current_user', methods=['GET', 'POST'])
# def current_user():
#     if current_user:


@login_manager.user_loader
def load_user(user_id):
    return UserLogin.get(user_id)