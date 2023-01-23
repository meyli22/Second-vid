from flask import render_template,redirect,url_for,flash, request
from shop import app,db
from .models import Category,Brand




@app.route('/addbrand',methods=['GET','POST'])
def addbrand():
    if request.method =="POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'The brand {getbrand} was added to your database','success')
        db.session.commit()
        return redirect(url_for('addbrand'))
     
    return render_template('products/addbrand.html', brands='brands')




@app.route('/addcat',methods=['GET','POST'])
def addcat():
    if request.method =="POST":
        getbrand = request.form.get('category')
        cat = Category(name=getbrand)
        db.session.add(cat)
        flash(f'The Category {getbrand} was added to your database','success')
        db.session.commit()
        return redirect(url_for('addbrand'))
     
    return render_template('products/addbrand.html')