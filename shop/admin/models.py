from shop import db
from flask import Flask
# from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
#primary key for the table and is of type integer
    name = db.Column(db.String(30),unique=False, nullable=False)
#string of length check validation with up to 30 characters and cannot be null
    username = db.Column(db.String(80), unique=True, nullable=False)
#string of length check validation with up to 80 characters and must be unique and not null.
    email = db.Column(db.String(120), unique=True, nullable=False)
#string of length check validation with up to 120 characters and must be unique and not null
    password = db.Column(db.String(180),unique=False, nullable=False)
#string of length check validation with up to 180 characters and cannot be null

    def __repr__(self):
        return '<User %r>' % self.username
#returns a string representation of the User object that includes the user's username.



def init_db():
    db.create_all()




        
