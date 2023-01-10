from app import db
from flask_login import UserMixin
import sqlalchemy as mod

class User(UserMixin, db.Model):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pwd = db.Column(db.String(300), nullable=False, unique=True)
    token = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Userdata(UserMixin, db.Model):
    __tablaname__ = "userdata"

    # username = db.Column(mod.ForeignKey(User.username), unique=True, primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    firstname= db.Column(db.String(30), default="Nill")
    lastname= db.Column(db.String(30), default="Nill")
    address= db.Column(db.String(120), default="Nill")
    address2= db.Column(db.String(120), default="Nill")
    city= db.Column(db.String(30), default="Nill")
    state= db.Column(db.String(30), default="Nill")
    zip= db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<User %r>' % self.username


class Leaderboard(UserMixin, db.Model):
    __tablaname__ = "Leaderboard"
    
    # username = db.Column(mod.ForeignKey(User.username), unique=True, primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    votes = db.Column(db.Integer, default=0)
    status = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return '<User %r>' % self.username