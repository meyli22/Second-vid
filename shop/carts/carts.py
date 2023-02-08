from flask import render_template,redirect,url_for,flash, request, session, current_app
from shop import app,db
from shop.products.models import Addproduct
#from shop.products.routes import brands
import json

def MagerDicts(dict1,dict2):
    if isinstance(dict1, list) and isinstance(dict2,list):
        return dict1  + dict2
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))


@app.route('/addcart', methods=['POST'])
def AddCart():
    try:
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity'))
        product = Addproduct.query.filter_by(id=product_id).first()
        if product_id and quantity and request.method =="POST":
#retrieves the product details from the database based on the product id
            DictItems = {product_id:{'name':product.name,'price':float(product.price),'quantity':quantity,'image':product.image_1}}
#creates a dictionary object with the product details
            if 'Shoppingcart' in session:
#stores it in the session under the key 'Shoppingcart'
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
#if the key is already in the session, it checks if the product id is also in the session
                    for key, item in session['Shoppingcart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            item['quantity'] += 1
#if it is, increments the quantity of the product in the cart
                    print("Sorry! This cigar is already in your cart")
                else:
                    session['Shoppingcart'] = MagerDicts(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)
            else:
#if the product is not in the session, it adds the dictionary object to the session
                session['Shoppingcart'] = DictItems 
                return redirect(request.referrer)
#redirects the admin user back to the previous page after adding the product to the cart.
    except Exception as e:
#catches any exception that is raised in the try block above
        print(e)
#if an exception occurs, the error message is printed 
    finally:
#executed after the try and except blocks, regardless of whether an exception was raised or not
        return redirect(request.referrer)
#returns the user to the previous page 

@app.route('/carts')
def getCart():
    if 'Shoppingcart' not in session: or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    subtotal = 0
    grandtotal = 0
    for key,product in session['Shoppingcart'].items():
        subtotal += float(product['price']) * int(product['quantity'])
        tax = ("%.2f" % (.10 * float(subtotal)))
        grandtotal = float("%.2f" % (1.10 * subtotal))
    return render_template('products/carts.html', tax = tax, grandtotal= grandtotal,brands=brands())

