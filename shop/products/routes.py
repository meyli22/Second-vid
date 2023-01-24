from flask import render_template,redirect,url_for,flash, request, session
from shop import app,db #, photos
from .models import Category,Brand, Addproduct
from .forms import Addproducts
import secrets

@app.route('/')
def home():
    return " "


@app.route('/addbrand',methods=['GET','POST'])
def addbrand():
    if request.method =="POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        #db.create_all()
        db.session.add(brand)
        flash(f'The brand {getbrand} was added to your database','success')
        db.session.commit()
        return redirect(url_for('addbrand'))
     
    return render_template('products/addbrand.html', brands='brands')
    
    #, brands='brands')

#db.create_all()
        # db.session.add(user)
        # db.session.commit()


# @app.route('/addcat',methods=['GET','POST'])
# def addcat():
#     if request.method =="POST":
#         getbrand = request.form.get('category')
#         cat = Category(name=getbrand)
#         db.session.add(cat)
#         flash(f'The Category {getbrand} was added to your database','success')
#         db.session.commit()
#         return redirect(url_for('addbrand'))
     
#     return render_template('products/addbrand.html')

@app.route('/addproduct', methods=['GET','POST'])
def addproduct():
    form = Addproducts(request.form)
    return render_template('products/addproduct.html', title='Add Cigar Page', form=form)
    