from src import db
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
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
    user_id = db.Column(db.Integer, db.ForeignKey(UserVisit.id), nullable=False)
    user = db.relationship(UserVisit)


# class Team(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), nullable=False, unique=True)
#     description = db.Column(db.String, nullable=False)
#     location = db.Column(db.String, nullable=False)
#     email= db.Column(db.String, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey(UserVisit.id), nullable=False)
#     create_at = db.Column(db.DateTime, )
#     isActive = db.Column(db.Boolean, default=False)
#     img_url= db.Column(db.String, nullable=True)
#     # members = db.Column()
#     # campaigns = db.Column()
#     # reviews = db.Column()

# class Campaigns(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), nullable=False, unique=True)
#     description = db.Column(db.String, nullable=False)
#     location = db.Column(db.String, nullable=False)
#     team_id = db.Column(db.Integer, db.ForeignKey(Team.id), nullable=True)
#     user_id = db.Column(db.Integer, db.ForeignKey(UserVisit.id), nullable=True)
#     create_at = db.Column(db.DateTime)
#     start_at = db.Column(db.DateTime)
#     end_at = db.Column(db.DateTime)
#     img_url = db.Column(db.String)
#     bank_id = db.Column(db.Integer, db.ForeignKey(Bank.id), default=None)
#     # donations = db.Column()
#     #members
#     #reviews

# class Review(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     rating = db.Column(db.Integer, nullable=True)
#     text = db.Column(db.String, nullable=True)
#     user_id = db.Column(db.Integer, db.ForeignKey(UserVisit.id), nullable=False)
#     team_id = db.Column(db.Integer, db.ForeignKey(Team.id))
#     campaign_id = db.Column(db.Integer, db.ForeignKey(Campaign.id))

# class Donation(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     amount = db.Column(db.String, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey(UserVisit.id), nullable=False)
#     campaign_id = db.Column(db.Integer, db.ForeignKey(Campaign.id))

# class Bank(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     provider = db.Column(db.String, nullable=False)
#     account_no = db.Column(db.Integer, nullable=False)
#     campaign_id = db.Column(db.Integer, db.ForeignKey(Campaign.id), nullable=False)

# class Location(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     address = db.Column(db.String)
#     lat = db.Column(db.Float)
#     long = db.Column(db.Float)
#     team_id = db.Column(db.Integer, db.ForeignKey(Team.id))
#     campaign_id = db.Column(db.Integer, db.ForeignKey(Campaign.id))


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
























