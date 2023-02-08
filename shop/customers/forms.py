from wtforms import Form, StringField, TextAreaField, PasswordField,SubmitField,validators, ValidationError
from flask_wtf.file import FileRequired,FileAllowed, FileField
from flask_wtf import FlaskForm
from .models import Register


class CustomerRegisterForm(FlaskForm):
    name = StringField('Name: ')
#text input field for the customer name
    username = StringField('Username: ', [validators.DataRequired()])
#text input field for the customer username. ensures that this field cannot be submitted empty
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
# text input field for the customer email. Check if the entered value is a valid email
#ensures it cant be submitted empty
    password = PasswordField('Password: ', [validators.DataRequired(), 
    validators.EqualTo('confirm', message=' Sorry! Please make sure both password match. ')])
#password input field for the customer password. Ensures it cant be submitted empty
#checks if the value entered matches the value entered in the "confirm" field.
    confirm = PasswordField('Repeat Password: ', [validators.DataRequired()])
#password input field for confirming the customer password. 
#ensures it cant be submitted empty
    country = StringField('Country: ', [validators.DataRequired()])
#text input field for the customer country. Ensures it cant be submitted empty
    contact = StringField('Contact: ', [validators.DataRequired()])
#text input field for the customer contact number. Ensures it cant be submitted empty
    address = StringField('Address: ', [validators.DataRequired()])
#text input field for the customer address
    zipcode = StringField('Zip code: ', [validators.DataRequired()])
#text input field for the customer zip code. 

    def validate_username(self, username):
        if Register.query.filter_by(username=username.data).first():
#checks if the inputted username already exists in the database
            raise ValidationError("Sorry! This username is already taken. Please select a different one")
#if it is found in the database, a "ValidationError" will be raised with the corresponding error message.
        
    def validate_email(self, email):
        if Register.query.filter_by(email=email.data).first():
#checks if the inputted email already exists in the database
            raise ValidationError("Sorry! This email address is taken. Please select a different one")
#if it is found in the database, a "ValidationError" will be raised with the corresponding error message.

    


class CustomerLoginFrom(FlaskForm):
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired()])



   




   

 

    

     

   


    
