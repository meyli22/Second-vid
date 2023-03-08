from flask import render_template,redirect,url_for,flash, request, session, current_app
from shop import app,db
from shop.products.models import Addproduct
import json
from flask_login import login_required

from math import log10, floor
import math

def MagerDicts(dict1,dict2):
    if isinstance(dict1, list) and isinstance(dict2,list):
        return dict1  + dict2
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))


@app.route('/addcart', methods=['POST'])
@login_required
def AddCart():
    try:
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity'))
        product = Addproduct.query.filter_by(id=product_id).first()

        if product_id and quantity and request.method =="POST":
            DictItems = {product_id:{'name':product.name,'price':float(product.price),'quantity':quantity,'image':product.image_1}}
            
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    print("Sorry! This cigar is already in your cart")
                else:
                    session['Shoppingcart'] = MagerDicts(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)

            else:
                session['Shoppingcart'] = DictItems 
                return redirect(request.referrer)

    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

def round_sig(x, sig=1):
    return round(x, sig-int(floor(log10(abs(x))))-1)

def round_to_n(x, n):
    if not x: return 0
    power = -int(math.floor(math.log10(abs(x)))) + (n - 1)
    factor = (10 ** power)
    return round(x * factor) / factor

@app.route('/carts')
def getCart():
    if 'Shoppingcart' not in session: 
        return redirect(request.referrer) 
    subtotal = 0
    grandtotal = 0
    for key,product in session['Shoppingcart'].items():
        # price = float(product['price'])
        # quantity = int(product['quantity'])
        # subtotal = price * quantity
        subtotal += float(product['price']) * int(product['quantity'])
        tax = ("%.2f" % (.10 * float(subtotal)))
        #tax = tax + round_to_n(0.1 * subtotal, 3)
        grandtotal = float("%.2f" % (1.10 * subtotal))
    return render_template('products/carts.html', tax = tax, grandtotal= grandtotal)