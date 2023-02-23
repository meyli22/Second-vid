from flask import render_template,redirect,url_for,flash, request, session, current_app
from shop import app,db, photos
from .models import Brand , Addproduct
from .forms import Addproducts
import secrets, os

# def brands():
#     brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
#     return brands

@app.route('/')
#associates the function with the URL endpoint '/'
def home():
    products = Addproduct.query.all()
#retrieves a list of all cigars from the database
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
#retrieves all of the brands, including the products associated with each brand.
    return render_template('products/index.html', products=products,brands=brands)
#pass the list of products and brands as arguments
#access the products and brands to display the information to the user



@app.route('/product/<int:id>')
#associates the function with the URL endpoint '/product/<int:id>'
def single_page(id):
    product = Addproduct.query.get_or_404(id)
#retrieves the product with the specified ID, or 404 error if the product is not found
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
#retrieves all of the brands, including the products associated with each brand
    return render_template('products/single_page.html',product=product,brands=brands)
#pass the product and brands as arguments
#access the product and brands in order to display the information to the user

@app.route('/brand/<int:id>')
def get_brand(id):
#takes the "id" argument passed in from the URL
    get_brand = Brand.query.filter_by(id=id).first_or_404()
#retrieves the brand object with the matching "id"
#if the brand object doesn't exist, a 404 error will be raised
    brand = Addproduct.query.filter_by(brand_id=id)
#retrieves all products that belong to the brand by filtering the "Addproduct" objects
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all() 
#brands object is created by joining the "Brand" and Addproduct tables on the id & brand_id columns 
    return render_template('products/index.html',brand=brand,brands=brands),get_brand=get_brand)
#receive the "brand" and "brands" objects as arguments
#used to display information about the brand and its products

@app.route('/addbrand',methods=['GET','POST'])
def addbrand():
    if 'email' not in session:
#checks if a user is logged in
        flash(f'Please to add a barnd you need to login first','danger')
        return redirect(url_for('login'))
#if not logged in redirects them to the login page
    if request.method =="POST":
        getbrand = request.form.get('brand')
#retrieves the name of the brand from the form data
        brand = Brand(name=getbrand)
#creates a new Brand object using that name
        db.session.add(brand)
#adds it to the database session
        flash(f'The brand {getbrand} was successfully added to your database','success')
        db.session.commit()
#commits the changes to the database
        return redirect(url_for('addbrand')) 
#redirects the user back to the addbrand page
    return render_template('products/addbrand.html', brands='brands')
    

@app.route('/addproduct', methods=['GET','POST'])
def addproduct():
     form = Addproducts(request.form)
#creates an instance of the Addproducts form
     brands = Brand.query.all()
#fetches all the brands from the database
     if request.method=="POST":
        name = form.name.data
        price = form.price.data
        stock = form.stock.data
        length = form.length.data
        strength = form.strength.data
        desc = form.description.data
        brand = request.form.get('brand')
#retrieves the form data and saves it to the database

        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + "." )
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + "." )
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + "." )
#saves three uploaded images with unique filenames to the local file system using
        addproduct = Addproduct(name=name,price=price, stock=stock,length=length, strength=strength,
                           desc=desc,brand_id=brand,image_1=image_1,image_2=image_2,image_3=image_3)
#creates an instance of the Addproduct model, populates it with the retrieved form data
        db.session.add(addproduct)
#adds it to the database 
        flash(f'The cigar {name} was added in database','success')
#flashes a success message
        db.session.commit()
#commits the changes to the database 
        return redirect(url_for('admin'))

     return render_template('products/addproduct.html', form=form, title='Add a Cigar', brands=brands)
#renders the template  with the form instance and the brands list as arguments

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

# @app.route('/result')
# def result():
#     searchword = request.args.get('q')
#     products = Addproduct.query.msearch(searchword, fields=['name','desc'] , limit=3)
#     return render_template('products/result.html',products=products)
#     #,brands=brands())
