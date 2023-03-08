from wtforms import Form,  StringField, PasswordField, validators 
from flask_wtf import FlaskForm

class RegistrationForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=25)])
#text input String field for the user's name. Has validation for a length between 4 & 25 characters
    username = StringField('Username', [validators.Length(min=4, max=25)])
#text input String field for the username. Has validation for a length between 4 & 25 characters
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.Email()])
#text input String field for the email. Validation for a length between 6 and 35 characters
#ensures is a valid address.
    password = PasswordField(' Password', [validators.DataRequired(), 
    validators.EqualTo('confirm', message='Passwords must match')])
#password input field. Validation of presence check and if it matches with the value in the confirm field.
    confirm = PasswordField('Repeat Password')
#password input field to confirm the password.

class LoginForm(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField(' Password', [validators.DataRequired()])