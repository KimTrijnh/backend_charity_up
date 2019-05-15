from src import db
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid


class UserVisit(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), unique=True)
    email = db.Column(db.String(256), unique=True)
    password_hash = db.Column(db.String(120))
    img_url = db.Column(db.String(300))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        UserVisit.id), nullable=False)
    user = db.relationship(UserVisit)


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    description = db.Column(db.String, nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_visit.id'), nullable=False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow, server_default= db.func.now())
    isActive = db.Column(db.Boolean, default=False)
    img_url = db.Column(db.String, nullable=True)
    # members = db.relationship('user_visit', backref='team', lazy=True)
    campaigns = db.relationship('Campaign', backref='team', lazy=True)
    reviews = db.relationship('Review', backref='team', lazy=True)
    

  
class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String, nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_visit.id'), nullable=True)
    created_at = db.Column(db.DateTime, default = datetime.utcnow, server_default= db.func.now())
    start_at = db.Column(db.DateTime, nullable=False, index=True)
    end_at = db.Column(db.DateTime, nullable=False, index=True)
    img_url = db.Column(db.String, nullable=True)
    isActive = db.Column(db.Boolean, default=False)
    bank_id = db.Column(db.Integer, db.ForeignKey('bank.id'), nullable=True)
    donations = db.relationship('Donation', backref='campaign', lazy=True)
    # members = db.relationship('user_visit', backref='team', lazy=True)
    reviews = db.relationship('Review', backref='campaign', lazy=True)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=True)
    text = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow, server_default= db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user_visit.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))

class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow, server_default= db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user_visit.id'), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)

class Bank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    provider = db.Column(db.String(40), nullable=False)
    account_no = db.Column(db.String(16), nullable=False)
    # campaign_id = db.Column(db.Integer, db.ForeignKey(Campaign.id), nullable=False)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String, nullable=False, index=True)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    campaigns = db.relationship('Campaign', backref='location', lazy=True)
    teams = db.relationship('Team', backref='location', lazy=True)

 

# class SubCampaign(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     campaign_id = db.Column(db.Integer, db.ForeignKey(Campaign.id))
#     start_at =
#     end_at =
#     location =

# # class Image(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     team_id
# #     user_id
# #     campaign_id
