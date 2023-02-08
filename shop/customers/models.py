from shop import db, login_manager
from datetime import datetime
from flask_login import UserMixin
import json
from flask_sqlalchemy import SQLAlchemy


@login_manager.user_loader
def user_loader(user_id):
    return Register.query.get(user_id)

class Register(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key= True)
#primary key integer column
    name = db.Column(db.String(50), unique= False)
#string column of length 50
    username = db.Column(db.String(50), unique= True)
#unique string column of length 50
    email = db.Column(db.String(50), unique= True)
#unique string column of length 50
    password = db.Column(db.String(200), unique= False)
#string column of length 200
    country = db.Column(db.String(50), unique= False)
#string column of length 50
    contact = db.Column(db.String(50), unique= False)
#string column of length 50
    address = db.Column(db.String(50), unique= False)
#string column of length 50
    zipcode = db.Column(db.String(50), unique= False)
#string column of length 50
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
# date-time column which records the date and time when the user was created

    def __repr__(self):
#provides a string representation of the Register model
        return '<Register %r>' % self.name
#returns the name of the user

class JsonEcodedDict(db.TypeDecorator):
    impl = db.Text
    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)
    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)


class CustomerOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20), default='Pending', nullable=False)
    customer_id = db.Column(db.Integer, unique=False, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    orders = db.Column(JsonEcodedDict)

    def __repr__(self):
        return'<CustomerOrder %r>' % self.invoice

db.create_all()

# def init_db():
#     db.create_all()
