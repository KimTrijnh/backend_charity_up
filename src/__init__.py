
from src.models import *
from flask import Flask, redirect, render_template, url_for, flash, jsonify, request
from flask_cors import CORS
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import login_required, current_user, LoginManager

app = Flask(__name__)
CORS(app)

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)


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
                'username': user.username
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
            return jsonify({'isLogin': True, 'current_user': user.username})
        else:
            return jsonify({'isLogin': False, 'message': 'Wrong Username/Password'})
    return redirect("http://localhost:3000/login")


@app.route('/team/create', methods=['POST'])
def create_team():
    if request.method == 'POST':
        data = request.get_json()
        team = Team(name=data['name'], description=data['description'], location=data['location'], email=data['email'], user_id=data['user_id'],
                    isActive=data['isActive'], img_url=data['img_url'])
        if team:
            db.sesson.add(team)
            db.session.commit()
            return jsonify({'success': True, 'team_id': team.id})
        else:
            return jsonify({'success': False, 'error': 'invalid input'})
    return jsonify({'message': 'invalid method'})


@app.route('/teams', methods=['GET'])
def teams():
    if request.method == 'GET':
        teams = Team.query.all()
        teamArray = []
        for team in teams:
            teamArray.append({
                'id' : team.id,
                'img_url': team.img_url,
                'name' : team.name,
                'description': team.description,
                'user_id' : team.user_id,
                'location': team.location,
                'create_at': team.create_at,
                'email': team.email,
                'isActive': team.isActive,
                'total_rating':
                'rating':
                'total_campaign':
                'total_member':
            })
        return jsonify({'success': True, teamArray})
    return jsonify({ 'success': False, 'message': 'invalid method'})


@app.route('/team/<int:id>', methods=['GET'])
def team(id):
    if request.method == 'GET':
        team = Team.query.filter_by(id=id).first()
        if team:
            teamDict = {
                'id' : team.id,
                'img_url': team.img_url,
                'name' : team.name,
                'description': team.description,
                'user_id' : team.user_id,
                'location': team.location,
                'create_at': team.create_at,
                'email': team.email,
                'isActive': team.isActive,
                'total_rating':
                'rating':
                'total_campaign':
                'total_member':
                }
            return jsonify({'success': True, 'team' : teamDict})
        else:
            return jsonify({'success': False, 'message': 'team not found'})
    return jsonify({'message': 'invalid method'})


@login_manager.user_loader
def load_user(user_id):
    return UserLogin.get(user_id)
