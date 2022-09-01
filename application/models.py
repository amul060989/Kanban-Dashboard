from enum import unique
from application.database import db

class Tasks(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, autoincrement=True, primary_key = True, nullable = False)
    summary = db.Column(db.String, nullable = False)
    description = db.Column(db.String)
    status = db.Column(db.String, nullable = False)

class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, autoincrement = True, primary_key = True, nullable = False, unique = True)
    username = db.Column(db.String, nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    f_name = db.Column(db.String, nullable = False)
    l_name = db.Column(db.String) 
