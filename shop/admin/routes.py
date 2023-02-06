from shop import app, db, bcrypt
from flask import render_template, session, request, redirect, url_for, flash


from .forms import RegistrationForm, LoginForm
from .models import User
from shop.products.models import  Brand, Addproduct
from flask_login import login_user

import os


@app.route('/admin')
def admin():
    if 'email' not in session:
        flash(f'Please to continue login first', 'danger')
        return redirect(url_for('login'))
    products = Addproduct.query.all()
    return render_template('admin/index.html', title='Admin Page', products=products)

# @app.route('/admin')
# def admin():
#     return render_template('product/catalogue', title='Catalogue', products=products)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)

        user = User(name=form.name.data, username=form.username.data, email=form.email.data, password=hash_password)
        db.create_all()
        db.session.add(user)
        db.session.commit()
        session['email'] = form.email.data
        flash(f' Welcome {form.name.data} !Thank you for registering', 'success')
        return redirect(url_for('login'))
    return render_template('admin/register.html', form=form, title="Registeration page")

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            paas = bcrypt.check_password_hash(user.password, form.password.data)
            print(paas)
            session['email'] = form.email.data
            flash(f'Welcome {form.email.data} You are logged in', 'success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash('wrong password. please try again', 'danger')
    return render_template('admin/login.html', form=form,title='Login Page')
    
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
