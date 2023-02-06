from flask import render_template,redirect,url_for,flash, request, session, current_app
from shop import app,db, photos
from .models import Brand , Addproduct
from .forms import Addproducts
import secrets, os

# def brands():
#     brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
#     return brands

@app.route('/')
def home():
    products = Addproduct.query.all()
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    #.filter(Addproduct.stock > 0)
    return render_template('products/index.html', products=products,brands=brands)

# @app.route('/result')
# def result():
#     searchword = request.args.get('q')
#     products = Addproduct.query.msearch(searchword, fields=['name','desc'] , limit=3)
#     return render_template('products/result.html',products=products)
#     #,brands=brands())

@app.route('/product/<int:id>')
def single_page(id):
    product = Addproduct.query.get_or_404(id)
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    return render_template('products/single_page.html',product=product,brands=brands )

@app.route('/brand/<int:id>')
def get_brand(id):
    get_brand = Brand.query.filter_by(id=id).first_or_404()
    brand = Addproduct.query.filter_by(brand_id=id)#(brand=get_brand).paginate(page=page, per_page=8)
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all() 
    return render_template('products/index.html',brand=brand,brands=brands)# ,categories=categories(),get_brand=get_brand)

@app.route('/addbrand',methods=['GET','POST'])
def addbrand():
    if 'email' not in session:
        flash(f'Please to add a barnd you need to login first','danger')
        return redirect(url_for('login'))
    if request.method =="POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        #db.create_all()
        db.session.add(brand)
        flash(f'The brand {getbrand} was successfully added to your database','success')
        db.session.commit()
        return redirect(url_for('addbrand')) 
    return render_template('products/addbrand.html', brands='brands')
    

@app.route('/addproduct', methods=['GET','POST'])
def addproduct():
     form = Addproducts(request.form)
     brands = Brand.query.all()
     if request.method=="POST":
        name = form.name.data
        price = form.price.data
        stock = form.stock.data
        length = form.length.data
        strength = form.strength.data
        desc = form.description.data
        brand = request.form.get('brand')

        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + "." )
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + "." )
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + "." )
        addproduct = Addproduct(name=name,price=price, stock=stock,length=length, strength=strength,desc=desc,brand_id=brand,image_1=image_1,image_2=image_2,image_3=image_3)
        db.session.add(addproduct)
        flash(f'The cigar {name} was added in database','success')
        db.session.commit()
        #return redirect(url_for('admin'))

     return render_template('products/addproduct.html', form=form, title='Add a Cigar', brands=brands)
    
# @app.route('/addproduct', methods=['GET','POST'])
# def addproduct():
#     form = Addproducts(request.form)
#     brands = Brand.query.all()
#     if request.method=="POST": #and 'image_1' in request.files:
#         photos.save(request.files.get('image_1'))
#         photos.save(request.files.get('image_2'))
#         photos.save(request.files.get('image_3'))
#         name = form.name.data
#         price = form.price.data
#         stock = form.stock.data
#         length = form.length.data
#         strength = form.strength.data
#         desc = form.discription.data
#         brand = request.form.get('brand')
#         image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
#         image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
#         image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
#         addproduct = Addproduct(name=name,price=price, stock=stock,length=length, strength=strength,desc=desc,brand_id=brand,image_1=image_1,image_2=image_2,image_3=image_3)
#         db.session.add(addproduct)
#         flash(f'The product {name} was added in database','success')
#         db.session.commit()
#         return redirect(url_for('admin'))
#     return render_template('products/addproduct.html', form=form, title='Add a Product', brands=brands) 
