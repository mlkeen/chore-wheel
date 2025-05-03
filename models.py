from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Household(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    users = db.relationship('User', backref='household', lazy=True)
    chores = db.relationship('Chore', backref='household', lazy=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    allowance_balance = db.Column(db.Integer, default=0)
    household_id = db.Column(db.Integer, db.ForeignKey('household.id'), nullable=False)
    chores = db.relationship('Chore', backref='assigned_user', lazy=True)

class Chore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    value = db.Column(db.Integer, nullable=False, default=0)
    is_complete = db.Column(db.Boolean, default=False)
    assigned_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    household_id = db.Column(db.Integer, db.ForeignKey('household.id'), nullable=False)
