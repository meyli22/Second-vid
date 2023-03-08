from flask import render_template,session, request,redirect,url_for,flash,current_app, make_response
from flask_login import login_required, current_user, logout_user, login_user
from shop import app,db,photos,bcrypt, login_manager
from .forms import CustomerRegisterForm, CustomerLoginFrom
from .models import Register, CustomerOrder
import secrets
import os
import json
import stripe

from math import log10, floor
import math

publishable_key = 'pk_test_51MiiqEG4Xz7PxOC0DmCEZCUIVyMzfmCTJekTNZk8w9oS2UBDWfQ7FvhWfmEMZ6ed2HxUB2XjUNKgW1huZ8NiASC0003aEUko2Z'
stripe.api_key = 'sk_test_51MiiqEG4Xz7PxOC02krtWyft4oJ9u1lsLjwL4MIxszCd0dPXAEAB9t7Wxw0i0eimUo0Qof0Jst2QqPSOTFXBcGXg00GPM0gIQI'


@app.route('/payment', methods=['POST'])
@login_required
def payment():
    invoice = request.form.get('invoice')
    stripe_token = request.form.get('stripeToken')
    return redirect(url_for('home'))

@app.route('/customer/register', methods=['GET','POST'])
def customer_register():
    form = CustomerRegisterForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name=form.name.data, username=form.username.data, email=form.email.data,password=hash_password,country=form.country.data,contact=form.contact.data, address=form.address.data, zipcode=form.zipcode.data)
        db.create_all()
        db.session.add(register)
        db.session.commit()
        flash(f'Welcome {form.name.data} Thank you for signing in!', 'success')
        return redirect(url_for('login'))
    return render_template('customer/register.html', form=form)

@app.route('/customer/login', methods=['GET','POST'])
def customerLogin():
    form = CustomerLoginFrom()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Congrats! You are logged in!', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        flash('Sorry! Incorrect email and password. Please try again.','danger')
        return redirect(url_for('customerLogin'))
            
    return render_template('customer/login.html', form=form)

@app.route('/customer/logout')
def customer_logout():
    logout_user()
    return redirect(url_for('home'))

    
@app.route('/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
    try:
        order = CustomerOrder(invoice=invoice, customer_id=customer_id, orders=session['Shoppingcart']) 
        db.session.add(order)
        print("Changes have been added to the database")
        db.session.commit()
        print("Changes have been committed to the database")
        order = CustomerOrder.query.all()
        session.pop('Shoppingcart')
        flash('Congrats! Your order has been sent successfully','success')
        print(order)
        return redirect(url_for('orders', invoice=invoice))
    except Exception as e:
        print("An exception occurred while committing the changes to the database: ", e)
        flash('Sorry! Something went wrong with your order', 'danger')
        return redirect(url_for('getCart'))
def index():
    try:
        db.session.query('1').all()
        return 'Database connection successful'
    except:
        return 'Database connection failed'

def round_sig(x, sig=2):
    return round(x, sig-int(floor(log10(abs(x))))-1)

def round_to_n(x, n):
    if not x: return 0
    power = -int(math.floor(math.log10(abs(x)))) + (n - 1)
    factor = (10 ** power)
    return round(x * factor) / factor

@app.route('/orders/<invoice>')
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        customer_id = current_user.id
        customer = Register.query.filter_by(id=customer_id).first()
        orders = CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).first()
        
        subTotal = 0
        tax = 0
        grandTotal = 0
        for _key, product in orders.orders.items():
            price = float(product['price'])
            quantity = int(product['quantity'])
            subTotal = price * quantity
             
            tax += round_sig(0.1 * subTotal)
            
            grandTotal += 1.1 * subTotal
            grandTotal = round(grandTotal, 1)

        
    else:
        return redirect(url_for('customerLogin'))
    return render_template('customer/order.html', invoice=invoice, tax=tax, subTotal=subTotal, grandTotal=grandTotal, customer=customer, orders=orders)