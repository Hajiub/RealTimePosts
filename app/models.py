from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    posts    = db.relationship('Post', backref='user', lazy=True)

    def __init__(self, username, password) -> None:
        self.username = username
        self.set_password(password)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, value):
        return check_password_hash(self.password, value)

    @property
    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False
        
    def __repr__(self):
        return '<User %r>' % self.username
        
class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    content = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)