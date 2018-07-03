from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True)
    pwdhash = db.Column(db.String(100))

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    descp = db.Column(db.String(100))
    content = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref=db.backref('article'))
    time = db.Column(db.DateTime, default=datetime.now)
    category = db.Column(db.String(10))
    thumbnail = db.Column(db.String(50))

    def __init__(self, title, descp, content, category, thumbnail):
        self.title = title
        self.content = content
        self.descp = descp
        self.category = category
        self.thumbnail = thumbnail
