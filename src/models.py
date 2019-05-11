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

    