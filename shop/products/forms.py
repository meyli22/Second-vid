from flask_wtf.file import FileField,FileRequired,FileAllowed
from wtforms import Form, SubmitField,IntegerField,FloatField, BooleanField, StringField,TextAreaField,validators

class Addproducts(Form):
    name = StringField('Name', [validators.DataRequired()])
#string field which takes the name of the product as input and is a mandatory field.
    price = FloatField('Price', [validators.DataRequired()])
#float field which takes the price of the product as input and is a mandatory field
    stock = IntegerField('Stock', [validators.DataRequired()])
#integer field which takes the stock of the product as input and is a mandatory field.
    length = StringField('Length', [validators.DataRequired()])
#string field which takes the length of the product as input and is a mandatory field
    strength = StringField('Strength', [validators.DataRequired()])
#string field which takes the strength of the product as input and is a mandatory field
    description  = TextAreaField('Description', [validators.DataRequired()])
#text area field which takes the description of the product as input and is a mandatory field.

    image_1 = FileField('Image 1', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'])])
    image_2 = FileField('Image 2', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'])])
    image_3 = FileField('Image 3', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'])])
#file field which take the images of the product as input and is a mandatory field. 
