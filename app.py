from flask import Flask, redirect  # from the module 'flask' import 'Flask" the class
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask_bcrypt import Bcrypt
from flask import flash
import os
from werkzeug.utils import secure_filename

# from PIL import _Image

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
# Flask class takes an arguement ' __name__'
# SQLAlchemy:this makes the interaction btwn python and DB smoother
# Flask-SQLAlchemy:this makes the interaction btwn flask and SQLAlchemy smoother

# To create a database: enter python in terminal,from app import db, db.create_all()  creates the database
# db.drop_all() deletes the table from the database

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///sokoni.sqlite"  # path to database

app.config['IMAGE_UPLOAD'] = "E:\class\Sokoni\static\images"  # dictionary

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


# create table for productspi
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    size = db.Column(db.INTEGER, unique=False, nullable=False)
    color = db.Column(db.String(100), nullable=False)
    price = db.Column(db.INTEGER, nullable=False)
    image = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return 'Name {}'.format(self.name)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    username = db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(100), unique=False, nullable=False)
    password = db.Column(db.String(128), unique=False, nullable=False)


# hashing passwrd
# username
# email
# passwod

@app.route('/')  # @ is a decorator - a function that determines what should happen to the code below it
# app is an object of the 'Flask' class
def index():
    return render_template('index.html', title='SOKONI')


# to show data on python onto html,use {{ }}

@app.route('/products', methods=['GET', 'POST'])
def getproducts():
    products = Product.query.all()  # get all products from db
    return render_template('products.html', products=products)


@app.route('/products/create', methods=['GET', 'POST'])
def products():
    if request.form and request.files:  # if request is post

        # grab form image/files
        uploaded_image = request.files['productimage']
        #grab image name
        filename = uploaded_image.filename
        #secure filename
        filename=secure_filename(filename)
        print(filename)
        #save image
        uploaded_image.save(os.path.join(app.config['IMAGE_UPLOAD'],filename))



        # grab form data
        name = request.form.get('productname')
        price = request.form.get('productprice')
        size = request.form.get('productsize')
        color = request.form.get('productcolor')


        # create a product instance/object
        product = Product(name=name, price=price, size=size, color=color)

        # save data into the db
        db.session.add(product)
        db.session.commit()
        flash('your Product has been successfully created!')

    # if user is not posting show them available products
    # get the products from the db
    products = Product.query.all()  # get all products from db
    print(products)

    return render_template('create.html', title='All Products', products=products)


# localhost:3000/products/2/
@app.route('/products/<int:product_id>/')  # handling a single product
def detail(product_id):
    # get a product with the above id
    product = Product.query.get(product_id)
    return render_template('detail.html', product=product)


@app.route('/products/update/<int:product_id>/', methods=['GET', 'POST'])  # handling a single product
def update(product_id):
    product = Product.query.get(product_id)

    if request.form:  # posting

        name = request.form.get('productname')
        size = request.form.get('productsize')
        price = request.form.get('productprice')
        color = request.form.get('productcolor')
        print(name, size, price, color)

        # to save data to db
        # assigning new values to product
        product.name = name
        product.size = size
        product.price = price
        product.color = color
        # save the new changes
        db.session.commit()
        flash('your Product has been successfully updated')
        # go back to the previous page
        return redirect('/products/update/{}/'.format(product_id))

    return render_template('update.html', product=product)


# to delete product
@app.route('/products/delete/<int:product_id>/')
def delete(product_id):
    # product = Product.query.get(product_id)
    product = Product.query.get(product_id)
    # print(product)
    db.session.delete(product)
    db.session.commit()
    return redirect('/products')


@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.form:
        # grab form data
        name = request.form.get('name')
        email = request.form.get('useremail')
        username = request.form.get('username')
        password = request.form.get('userpassword')
        password_hash = bcrypt.generate_password_hash(password)
        print(name, email, username, password_hash)

        user = User(name=name, username=username, email=email, password=password_hash)
        return render_template('login.html')
    return render_template('registration.html')


# @app.route('/upload')
# def upload_file():
#     return render_template('upload.html')
#
#
# @app.route('/uploader', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         f = request.files['file']
#         f.save(secure_filename(f.filename))
#         return 'file uploaded successfully'


@app.route('/products/shoes')
def shoes():
    return 'Shoes Page'


@app.route('/products/shoes/<int:id>')  # int- specifies data type int;if not specified then string by default
def shoes_detail(id):
    return 'Shoes Page for id ' + str(id)


@app.route('/products/shoes/<name>/<int:id>')  # int- specifies data type int;if not specified then string by default
def shoes_detail2(name, id):
    return 'Shoes Page for {} with id {} '.format(name, id)


if __name__ == '__main__':
    app.run(port=8000, debug=True)

# pip freeze - checks the dependancies available in the virtual environment; if flask not available, pip install flask

# Codes used by server and browser:
# 200- success
# 404- not found
# 500- error in server

# Create a list of dictionaries:
# 'name':'Jordan'
# 'size':45
# 'colour':black
# 'price':2000
