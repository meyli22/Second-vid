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
            flash(f'Welcome {form.name.data} You are logged in', 'success')
            return redirect(url_for('admin'))
        else:
            flash('wrong password. please try again', 'danger')
    return render_template('admin/login.html', form=form,title='Login Page')