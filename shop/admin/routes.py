from shop import app, db, bcrypt
from flask import render_template, session, request, redirect, url_for, flash


from .forms import RegistrationForm, LoginForm
from .models import User
from shop.products.models import  Brand, Addproduct
from flask_login import login_user

import os


@app.route('/admin')
#creates a route for the Flask web application. When a user visits the '/admin' URL, the admin() function is executed
def admin():
    if 'email' not in session:
#checks if the 'email' key exists in the current session. If not, a message with a danger level is flashed 
        flash(f'Please to continue login first', 'danger')
        return redirect(url_for('login'))
#the user is redirected to the 'login' URL
    products = Addproduct.query.all()
#if the user is logged in, the function fetches all products from the database and passes the data to the render method 
    return render_template('admin/index.html', title='Admin Page', products=products)
#the template at 'admin/index.html' is rendered and returned to the user's browser.

# @app.route('/admin')
# def admin():
#     return render_template('product/catalogue', title='Catalogue', products=products)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
#validates the data submitted in the form 
        hash_password = bcrypt.generate_password_hash(form.password.data)
#if the form data is valid, a password hash is generated and a new user is created

        user = User(name=form.name.data, username=form.username.data, email=form.email.data, password=hash_password)
        db.create_all()
        db.session.add(user)
        db.session.commit()
#new user is added to the database session and committed
        session['email'] = form.email.data
#user's email is stored in a session variable
        flash(f' Welcome {form.name.data} !Thank you for registering', 'success')
        return redirect(url_for('login'))
#success message is displayed after the user has registered, and they are redirected to the login page.

    return render_template('admin/register.html', form=form, title="Registeration page")

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
#form is validated when the user submits it
        user = User.query.filter_by(email=form.email.data).first()
#the entered email is used to search for a user in the database.
        if user and bcrypt.check_password_hash(user.password, form.password.data):
#if a matching user is found, the entered password is checked against the hashed 
#password stored in the database 
            session['email'] = form.email.data
            flash(f'welcome {form.email.data} you are logedin now','success')
            return redirect(url_for('admin'))
#if the password matches, the user is logged in and redirected to the "admin" page
        else:
#if the password does not match or the user is not found, a message is displayed 
#indicating that the login attempt was unsuccessful
            flash(f'Wrong email and password', 'success')
            return redirect(url_for('login'))
    return render_template('admin/login.html',title='Login page',form=form)
#returns a template for the login page with the form
    
    # if request.method=="POST" and form.validate():
    #     email = request.form.get('email')
    #     password = request.form.get('password')
    #     user = User.query.filter_by(email = form.email.data).first()
        # user = User.query.filter_by(email=email).first()
        # if user:
        #     if bcrypt.check_password_hash(user.password, form.password.data):
        #         flash('Congratulations! You have logged in successfully!', category='success')
        #         login_user(user, remember=True)
        # if user and bcrypt.check_password_hash(user.password, form.password.data):
            # session['email'] = form.email.data
            # db.session.commit()
            # flash(f'welcome {form.email.data} you are logged in now','success')
    #             return redirect(url_for('/'))
            
    #         else:
    #             flash('Sorry! The password seems to be incorrect. Please try again.', category='error')
    #         #flash(f'Wrong email and password', 'danger') 
    #     else:
    #         flash('Sorry! This email does not exist.', category='error') 
            
    # return render_template('admin/login.html',form=form, title='Login page',)
