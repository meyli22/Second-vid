from flask_wtf.file import FileField,FileRequired,FileAllowed
from wtforms import Form, SubmitField,IntegerField,FloatField, BooleanField, StringField,TextAreaField,validators

class Addproducts(Form):
    name = StringField('Name', [validators.DataRequired()])
    price = FloatField('Price', [validators.DataRequired()])
    stock = IntegerField('Stock', [validators.DataRequired()])
    length = StringField('Length', [validators.DataRequired()])
    strength = StringField('Strength', [validators.DataRequired()])
    description  = TextAreaField('Description', [validators.DataRequired()])

    image_1 = FileField('Image 1', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'])])
    image_2 = FileField('Image 2', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'])])
    image_3 = FileField('Image 3', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'])])