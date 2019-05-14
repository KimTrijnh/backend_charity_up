
from flask import Flask, redirect, render_template, url_for, flash, jsonify, request
from flask_cors import CORS
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import login_required, current_user, LoginManager
from flask_moment import Moment


app = Flask(__name__)
CORS(app)

app.config.from_object(Config)
db = SQLAlchemy(app)
moment = Moment(app)
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
            team = Team.query.filter_by(user_id=user.id).first()
            if team:
                teamJson =  {'id': team.id, 'name': team.name}
            else:
                teamJson = {}
            return jsonify({'isLogin': True, 'current_user': user.username, 'team': teamJson})
        else:
            return jsonify({'isLogin': False, 'message': 'Wrong Username/Password'})
    return redirect("http://localhost:3000/login")


# CREATE VIEWS
@app.route('/team/create', methods=['POST', 'GET'])
def create_team():
    if request.method == 'POST':
        data = request.get_json()
        location = Location(address=data['location']['address'], lat = data['location']['lat'], lng = data['location']['lng'])
        db.session.add(location)
        db.session.commit()
        creater = UserVisit.query.filter_by(username=data['creater']).first()
        team = Team.query.filter_by(name=data['name']).first()
        if team:
            return jsonify({'success': False, 'error': "team's name is already taken"})
        else:
            team = Team(name=data['name'], description=data['description'], location_id=location.id, email=data['email'], user_id= creater.id,
                    isActive=data['isActive'], img_url=data['img_url'])
            if team:
                db.session.add(team)
                db.session.commit()
                return jsonify({'success': True, 'team_id': team.id})
            else:
                return jsonify({'success': False, 'error': 'invalid input'})
    return jsonify({'message': 'invalid method'})


@app.route('/campaign/create', methods=['GET', 'POST'])
def create_campaign():
    if request.method == 'POST':
        data = request.get_json()
        location = Location(address=data['location']['address'], lat = data['location']['lat'], lng = data['location']['lng'])
        if data['isDonated']:
            bank = Bank(provider=data['bank_name'], account_no=data['account_no'])
            bank_id = bank.id
            db.session.add(bank)
        else:
            bank_id = None      
        user = UserVisit.query.filter_by(username=data['current_user']).first()
        db.session.add(location)
        db.session.commit()
        if data['team_name']:
            team = Team.query.filter_by(name=data['team_name']).first()
        else:
            team = None

        campaign = Campaign(name=data['campaign_name'], description=data['description'], location_id=location.id, start_at=data['start_at'], end_at=data['end_at'], isActive=data['isActive'], bank_id=bank_id, img_url=data['img_url'])
        if campaign:
            db.session.add(campaign)
            db.session.commit()
            return jsonify({'success': True, 'campaign': {'id': campaign.id, 'name': campaign.name}, 'team': data['team_name']})
        else:
            return jsonify({'success': False, 'error': 'invalid input'})
        
    return jsonify({'message': 'invalid method'})


#TEAM VIEWS
# @app.route('/teams', methods=['GET'])
# def teams():
#     if request.method == 'GET':
#         teams = Team.query.all()
#         teamArray = []
#         for team in teams:
#             teamArray.append({
#                 'id' : team.id,
#                 'img_url': team.img_url,
#                 'name' : team.name,
#                 'description': team.description,
#                 'user_id' : team.user_id,
#                 'location': team.location,
#                 'create_at': team.create_at,
#                 'email': team.email,
#                 'isActive': team.isActive,
#                 'total_rating':
#                 'rating':
#                 'total_campaign':
#                 'total_member':
#             })
#         return jsonify({'success': True, teamArray})
#     return jsonify({ 'success': False, 'message': 'invalid method'})


# @app.route('/team/<int:id>', methods=['GET'])
# def team(id):
#     if request.method == 'GET':
#         team = Team.query.filter_by(id=id).first()
#         if team:
#             teamDict = {
#                 'id' : team.id,
#                 'img_url': team.img_url,
#                 'name' : team.name,
#                 'description': team.description,
#                 'user_id' : team.user_id,
#                 'location': team.location,
#                 'create_at': team.create_at,
#                 'email': team.email,
#                 'isActive': team.isActive,
#                 'total_rating':
#                 'rating':
#                 'total_campaign':
#                 'total_member':
#                 }
#             return jsonify({'success': True, 'team' : teamDict})
#         else:
#             return jsonify({'success': False, 'message': 'team not found'})
#     return jsonify({'message': 'invalid method'})


#CAMPAIGN VIEWS
@login_manager.user_loader
def load_user(user_id):
    return UserLogin.get(user_id)
