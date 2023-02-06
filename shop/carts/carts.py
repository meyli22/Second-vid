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
            DictItems = {product_id:{'name':product.name,'price':float(product.price),'quantity':quantity,'image':product.image_1}}
            
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    print("Sorry! This cigar is already in your cart")
                else:
                    session['Shoppingcart'] = MagerDicts(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)

                    
        #             for key, item in session['Shoppingcart'].items():
        #                 if int(key) == int(product_id):
        #                     session.modified = True
                    
        #           item['quantity'] += 1

            else:
                session['Shoppingcart'] = DictItems #MagerDicts(session['Shoppingcart'], DictItems)
                return redirect(request.referrer)
        #     else:
        #         session['Shoppingcart'] = DictItems
        #         return redirect(request.referrer)
              
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

@app.route('/carts')
def getCart():
    if 'Shoppingcart' not in session: #or len(session['Shoppingcart']) <= 0:
        return redirect(request.referrer) #(url_for('home'))
    subtotal = 0
    grandtotal = 0
    for key,product in session['Shoppingcart'].items():
        subtotal += float(product['price']) * int(product['quantity'])
        tax = ("%.2f" % (.10 * float(subtotal)))
        grandtotal = float("%.2f" % (1.10 * subtotal))
    return render_template('products/carts.html', tax = tax, grandtotal= grandtotal)
     #,brands=brands()

