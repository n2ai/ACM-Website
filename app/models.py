from datetime import datetime
from app.database import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

Base = declarative_base()


#class User(db.Model):
   # created_at = db.Column(db.DateTime, default=datetime.utcnow)
class UserAccount(db.Model):
    member_number = db.Column(db.Integer, db.ForeignKey('user_account.member_number'), primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    affiliation = db.Column(db.String(120), nullable=True)
    membership_type = db.Column(db.String(64), nullable=True)
    date_added = db.Column(db.String(10), default=datetime.utcnow().strftime('%Y-%m-%d'), nullable=True)
    expiration_date = db.Column(db.DateTime, nullable=True)
    active_acm_member = db.Column(db.Boolean, nullable=True)
#main user account table ^^


class UserPassword(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(128))
    user_account_id = db.Column(db.Integer, db.ForeignKey('user_account.member_number'), nullable=False)
    email = db.Column(db.String(120), db.ForeignKey('user_account.email'), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    @login.user_loader
    def load_user(id):
        return UserPassword.query.get(int(id))
    
    
#table with forbidden date x_x


class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return '<UserPassword {}>'.format(self.email)
    
class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    image_url = db.Column(db.String(256), nullable=False)


class Trending(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    image_url = db.Column(db.String(256), nullable=False)

class Events(db.Model):
    title = db.Column(db.String(128),primary_key=True, nullable=False)
    summary = db.Column(db.String(128), nullable=False)
    presenter = db.Column(db.String(128), nullable=False)
    place = db.Column(db.String(128), nullable=False)
    time = db.Column(db.String(15), nullable=False)
    date = db.Column(db.String(15), nullable=False)
    #contact_number = db.Column(db.String(16), nullable=False)
    #contact_email = db.Column(db.String(64), nullable=False)