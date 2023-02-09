from shop import db, app

from datetime import datetime


class Addproduct(db.Model):
#defines a new class. Inherits from db.Model
    id = db.Column(db.Integer, primary_key=True)
#primary key for the product of type Integer, ensures uniqueness.
    name = db.Column(db.String(80), nullable=False)
#text input field for product name of type String. Cant be empty
    price = db.Column(db.Numeric(10,2), nullable=False)
#text input field for product price of type Numeric. Cant be empty
    stock = db.Column(db.Integer, nullable=False)
#text input field for product stock of type Integer. Cant be empty
    length = db.Column(db.Integer, nullable=False)
#text input field for product length of type Integer. Cant be empty
    strength = db.Column(db.Text, nullable=False)
#text input field for product strength of type Text. Cant be empty
    desc = db.Column(db.Text, nullable=False)
#text input field for product description of type Text. Cant be empty
    pub_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
#stores the date and time the product was added to the database

    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'),nullable=False)
#integer column that stores the foreign key reference to the "brand" table
    brand = db.relationship('Brand',backref=db.backref('brands', lazy=True))

    image_1 = db.Column(db.String(150), nullable=False, default='image1.jpg')
    image_2 = db.Column(db.String(150), nullable=False, default='image2.jpg')
    image_3 = db.Column(db.String(150), nullable=False, default='image3.jpg')
#stores file paths to images of the product

    def __repr__(self):
        return '<Addproduct %r>' % self.name
#displays information about the cigar when it is printed


class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
#integer primary key
    name = db.Column(db.String(30), nullable=False, unique=True)
#string with a maximum length of 30 characters, unique
    def __repr__(self):
        return '<Brand %r>' % self.name
#should be represented as a string, for debugging purposes

with app.app_context():
    db.create_all()

def init_db():
    db.create_all()

# from flask_sqlalchemy import SQLAlchemy
# from flask import Flask
# from shop import app


# db = SQLAlchemy()

# class Brand(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(30), nullable=False, unique=True)

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myshop.db'



# def init_db():
#     db.create_all()

#db.create_all()


