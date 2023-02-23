from flask import render_template,session, request,redirect,url_for,flash,current_app,make_response
from flask_login import login_required, current_user, logout_user, login_user
from shop import app,db,photos,bcrypt, login_manager
from .forms import CustomerRegisterForm, CustomerLoginFrom
from .models import Register, CustomerOrder
import secrets
import os

@app.route('/customer/register', methods=['GET','POST'])
def customer_register():
    form = CustomerRegisterForm()
    if form.validate_on_submit():
#if the form is valid, it will hash the password using the bcrypt library
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name=form.name.data, username=form.username.data, email=form.email.data,password=hash_password,
                            country=form.country.data,contact=form.contact.data, address=form.address.data, zipcode=form.zipcode.data)
#create a Register object with the form data
        db.create_all()
        db.session.add(register)
        db.session.commit()
#add it to the database, and commit the changes
        flash(f'Welcome {form.name.data} Thank you for signing in!', 'success')
#the user is then shown a flash message to indicate successful registration
        return redirect(url_for('login'))
#redirected to the login page
    return render_template('customer/register.html', form=form)
#renders the template with a form object passed to it

@app.route('/customer/login', methods=['GET','POST'])
def customerLogin():
    form = CustomerLoginFrom()
#creates an instance of the CustomerLoginFrom class and performs form validation
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
#retrieves the user data from the database based on the entered email address
        if user and bcrypt.check_password_hash(user.password, form.password.data):
#check if the password entered by the user matches the hashed password stored in the database
            login_user(user)
#if they match, the function logs the user 
            flash('Congrats! You are logged in!', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
#redirects the user to the home page with a success message
        flash('Sorry! Incorrect email and password. Please try again.','danger')
#if the login fails, the function redirects the user back to the login page with a danger message
        return redirect(url_for('customerLogin'))
            
    return render_template('customer/login.html', form=form)

@app.route('/customer/logout')
#creates a route for the logout functionality
def customer_logout():
    logout_user()
#makes sure that the user session is ended and
#all the user data related to the session is cleared
    return redirect(url_for('home'))

# @app.route('/getorder')
# @login_required
# def get_order():
#     if current_user.is_authenticated:
#         customer_id = current_user.id
#         invoice = secrets.token_hex(5)
#         try:
#             order = CustomerOrder(invoice=invoice,customer_id=customer_id,orders=session['Shoppingcart'])
#             db.create_all()
#             db.session.add(order)
#             db.session.commit()
#             session.pop('Shoppingcart')
#             flash('Congrats! Your order has been sent successfully','success')
#             return redirect(url_for('home'))
            #'orders',invoice=invoice))
@app.route('/getorder')
@login_required
#only executes if the user is logged in
def get_order():
    if current_user.is_authenticated:
     customer_id = current_user.id
#retrieves the ID of the currently logged in user
     invoice = secrets.token_hex(5)
#generates a random hexadecimal string as an invoice number 
    try:
        order = CustomerOrder(invoice=invoice,customer_id=customer_id,orders=session['Shoppingcart'])
#creates a CustomerOrder object and sets its attributes to the invoice, customer_id, and orders value
        db.session.add(order)
        db.session.commit()
#adds the object to the database session and commits the transaction
        session.pop('Shoppingcart')
#Deletes the items in the shopping cart
        flash('Congrats! Your order has been sent successfully','success')
#Shows a flash message indicating that the order has been sent successfully
        return redirect(url_for('home'))
#Redirects the user to the home page
    except Exception as e:
            print(e)
#print the error message
            flash('Sory! Some thing went wrong with your order', 'danger')
#show a flash message indicating that something went wrong with the order
            return redirect(url_for('getCart'))
#user is then redirected to the getCart route


        # except Exception as e:
        #     print(e)
        #     flash('Sory! Some thing went wrong with your order', 'danger')
        #     return redirect(url_for('getCart'))

@app.route('/orders/<invoice>')
@login_required
#ensures that the user must be authenticated before accessing this page
def orders(invoice):
    if current_user.is_authenticated:
#checks if the user is authenticated
        grandTotal = 0
        subTotal = 0
        customer_id = current_user.id
#gets the ID of the current user from the current_user object
        customer = Register.query.filter_by(id=customer_id).first()
#queries the Register table in the database to retrieve the user object matching the customer_id.
        orders = CustomerOrder.query.filter_by(customer_id=customer_id).first(), invoice=invoice).order_by(CustomerOrder.id.desc()).first()
#queries the CustomerOrder table in the database to retrieve the order object matching the customer_id.
        for _key, product in orders.orders.items():
#loops through each item in the orders object
            subTotal == float(product['price']) * int(product['quantity'])
#calculates the subtotal by multiplying the price and quantity of each item in the order
            tax = ("%.2f" % (.10 * float(subTotal)))
#calculates the tax amount at a rate of 10% of the subtotal.
            grandTotal = ("%.2f" % (1.10 * float(subTotal)))
#calculates the grand total by adding the tax amount to the subtotal

    else:
        return redirect(url_for('customerLogin'))
    return render_template('customer/order.html', invoice=invoice, tax=tax,subTotal=subTotal,grandTotal=grandTotal,customer=customer,orders=orders)

  ----
@app.route('/payment',methods=['POST'])
#creates a route to the URL "/payment"
def payment():
    invoice = request.get('invoice')
#retrieves the "invoice" value from the request and stores it in a variable
    amount = request.form.get('amount')
#retrieves the "amount" value from the form data and stores it in a variable
    customer = stripe.Customer.create(
      email=request.form['stripeEmail'],
      source=request.form['stripeToken'],
    )
#creates a new customer in the Stripe system
#The resulting customer object is stored in a variable named
    charge = stripe.Charge.create(
      customer=customer.id,
      description='Myshop',
      amount=amount,
      currency='usd',
    )
#creates a new charge for the customer in the Stripe system
#resulting charge object is stored in a variable named
    orders =  CustomerOrder.query.filter_by(customer_id = current_user.id,invoice=invoice).order_by(CustomerOrder.id.desc()).first()
#retrieves the latest order for the current user from the database.  The resulting order object is stored in a variable
    orders.status = 'Paid'
#updates the "status" attribute of the "orders" object to "Paid"
    db.session.commit()
#saves the changes made to the database
    return redirect(url_for('home'))
#redirects the user back to the home page
       
