'''
CS3250 - Software Development Methods and Tools - Fall 2023
Instructor: Thyago Mota
Group Name: Backroom Gang
Description: Project01 - Routes for the SQLAlchemy Windoors Web App
'''

from app import app, db, load_user
from app.models import User, Reseller, Admin, Product, Order, Item
from app.forms import SignInForm, OrderForm, ItemForm, ResellerSignUpForm, AdminSignUpForm, OrderCreateForm, UpdateOrder, ChangeStatusForm
from flask import render_template, redirect, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
import bcrypt
from datetime import datetime

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index(): 
    return render_template('index.html')

############################################# USER AUTHENTICATION #############################################
# Done
@app.route('/users/signin', methods=['GET', 'POST'])
def users_signin():
    """ This function is used to sign in a user into the database"""
    #This purpose of this function is to sign in the user by checking if the user exists and if the password is correct 
    form = SignInForm() # This line's purpose is to create a new SignInForm object
    if form.validate_on_submit(): # This line's purpose is to check if the form has been submitted
        user = User.query.filter_by(id=form.id.data).first() # This line's purpose is to check if the user exists
        if user and bcrypt.checkpw(form.passwd.data.encode('utf-8'), user.passwd): # This line's purpose is to check if the password is correct
            login_user(user) # This line's purpose is to sign in the user
            return redirect(url_for('orders')) # This line's purpose is to redirect the user to the list of users page
    return render_template('users_signin.html', form = form) # This line's purpose is to render the sign in page

# Done
@app.route('/register_reseller', methods=['GET', 'POST'])
def register_reseller():
    """ This function is used to register a new reseller user into the database"""
    form = ResellerSignUpForm()
    if form.validate_on_submit():
        existing_user = Reseller.query.filter_by(id=form.id.data).first() 
        if existing_user:
            return '<p>User with that ID already exists!</p>' # This line's purpose is to return an error message if the user already exists

        passwd = form.passwd.data # This line's purpose is to append the password field to the SignUp form
        passwd_confirm = form.passwd_confirm.data # This line's purpose is to append the password confirmation field to the SignUp form
        
        if passwd == passwd_confirm: # This line's purpose is to check if the password and password confirmation fields match
            salt_passwd = bcrypt.gensalt() # This line's purpose is to generate a salt for the password
            
            hashed_passwd = bcrypt.hashpw(passwd.encode('utf-8'), salt_passwd) # This line's purpose is to hash the password
            Reselleruser = Reseller(id=form.id.data, email = form.email.data, creation_date = form.creation_date.data, company = form.company.data, address =form.address.data, phone = form.phone.data, website = form.website.data, passwd = hashed_passwd, role= "reseller") # This line's purpose is to create a new user
            
            db.session.add(Reselleruser) # This line's purpose is to add the new user to the database
            db.session.commit() # This line's purpose is to commit the new user to the database
        else:
            return '<p>Passwords do not match!</p>' # This line's purpose is to return an error message if the passwords do not match
        return redirect(url_for('users_signin')) # This line's purpose is to redirect the user to the sign in page
    return render_template('reseller_signup.html', form=form)

# Done
@app.route('/register_admin', methods=['GET', 'POST'])
def register_admin():
    """ This function is used to register a new admin user into the database"""
    form = AdminSignUpForm()
    if form.validate_on_submit():
        existing_user = Admin.query.filter_by(id=form.id.data).first() 
        if existing_user:
            return '<p>User with that ID already exists!</p>' # This line's purpose is to return an error message if the user already exists

        passwd = form.passwd.data # This line's purpose is to append the password field to the SignUp form
        passwd_confirm = form.passwd_confirm.data # This line's purpose is to append the password confirmation field to the SignUp form
        
        if passwd == passwd_confirm: # This line's purpose is to check if the password and password confirmation fields match
            salt_passwd = bcrypt.gensalt() # This line's purpose is to generate a salt for the password
            
            hashed_passwd = bcrypt.hashpw(passwd.encode('utf-8'), salt_passwd) # This line's purpose is to hash the password
            Adminuser = Admin(id=form.id.data, name = form.name.data, title = form.title.data, email = form.email.data, creation_date = form.creation_date.data, passwd = hashed_passwd, role= 'admin') # This line's purpose is to create a new user
            
            db.session.add(Adminuser) # This line's purpose is to add the new user to the database
            db.session.commit() # This line's purpose is to commit the new user to the database
        else:
            return '<p>Passwords do not match!</p>' # This line's purpose is to return an error message if the passwords do not match
        return redirect(url_for('users_signin'))
    return render_template('admin_signup.html', form=form)

# Done
@app.route('/users/signout', methods=['GET', 'POST'])
def users_signout():
    logout_user() # this function is used to sign out the user
    return redirect(url_for('index')) # this function is used to redirect the user to the index page

############################################# USER AUTHENTICATION #############################################

@app.route('/orders')
@login_required
def orders(): # COMPLETE  
    # Resellers must be able to track their own orders
    # Admin users must be able to track all orders
    
    if current_user.role == "admin" : # This line's purpose is to check if the current user is an admin
        all_orders = Order.query.all() # This line's purpose is to get the list of all orders
        return render_template('admin_orders.html', orders = all_orders) # This line's purpose is to render the orders page with the list of all orders
    else: # This line's purpose is to check if the current user is a reseller
        reselleruser_orders = Order.query.filter_by(reseller_id=current_user.id).all() # This line's purpose is to get the list of orders from the signed-in reselleruser (current_user)
        return render_template('orders.html', orders = reselleruser_orders) # This line's purpose is to render the orders page with the list of orders from the signed-in user (current_user)

    if current_user == Admin(): # This line's purpose is to check if the current user is an admin
        all_orders = Order.query.all() # This line's purpose is to get the list of all orders
        return render_template('orders.html', orders = all_orders) # This line's purpose is to render the orders page with the list of all orders
    elif current_user == Reseller(): # This line's purpose is to check if the current user is a reseller
         reselleruser_orders = Order.query.filter_by(reseller_id=current_user.id).all() # This line's purpose is to get the list of orders from the signed-in reselleruser (current_user)
         return render_template('orders.html', orders = reselleruser_orders) # This line's purpose is to render the orders page with the list of orders from the signed-in user (current_user)
    else:
         return redirect(url_for('index'))
    
# Done  
@app.route('/orders/create', methods=['GET','POST']) # This line's purpose is to create a new route for the create order page
@login_required
# Feature: Resellers must be able to place new orders through the platform.
# RESELLERS CAN ONLY CREATE ORDERS FOR THEMSELVES
# if the current user is not a reseller, redirect to the orders page
def orders_create():
    """ This function is used to create a new order into the database and add it to the list of orders
    where the current user is the reseller"""
    if current_user.role == "reseller": # This line's purpose is to check if the current user is a reseller
        form = OrderCreateForm() # This line's purpose is to create a new OrderForm object

        if request.method == 'GET': # This line's purpose is to check if the request method is GET
            initial_products = app.config['INITIAL_PRODUCTS'] # This line's purpose is to get the list of initial products from the app config

            for initial_product in initial_products: # This line's purpose is to iterate through the list of initial products
                form.products.append_entry(initial_product) # This line's purpose is to append the initial product to the list of products in the form

        if form.validate_on_submit(): # This line's purpose is to check if the form has been submitted
            order_number = generate_order_number() # This line's purpose is to generate the order number
            creation_date = generate_create_date() # This line's purpose is to generate the creation date
            product_entries = form.products.data # This line's purpose is to get the list of products from the form
            items = [] # This line's purpose is to create a new list of items
            items_product_codes = [] # This line's purpose is to create a new list of items product codes
            items_quantity = [] # This line's purpose is to create a new list of items quantity

            default_status = "New" # This line's purpose is to set the default status to "New"

            for product_entry in product_entries:
                product_code = product_entry['product_code'] # This line's purpose is to get the product code from the product entry
                quantity = product_entry['quantity'] # This line's purpose is to get the quantity from the product entry
                specs = product_entry['specs'] # This line's purpose is to get the specs from the product entry
                print(f"Processing product: {product_code}, Quantity: {quantity}, Specs: {specs}")

                if product_entry['quantity'] > 0: # This line's purpose is to check if the quantity is less than or equal to 0
                    # Create a new Item object for this product
                    new_item = Item(product_code=product_code, quantity=quantity, specs=specs) # This line's purpose is to create a new item
                    
                    items.append(new_item) # This line's purpose is to append the new item to the new order
                    items_product_codes.append(product_code) # This line's purpose is to append the product code to the list of items product codes
                    items_quantity.append(quantity) # This line's purpose is to append the quantity to the list of items quantity
                    print(f"Item created and appended to items list: {new_item}") # This line's purpose is to print the new item- PLACEHOLDER, REMOVE WHEN DONE
            
            print(f"Total items for this order: {len(items)}") # This line's purpose is to print the total number of items for this order- PLACEHOLDER, REMOVE WHEN DONE
            new_Order = Order(number=order_number, creation_date=creation_date, items=items, status=default_status, reseller_id=current_user.id) # This line's purpose is to create a new order
            new_Order.items = items # This line's purpose is to set the items of the new order to the list of items
            print(items_product_codes + items_quantity) # This line's purpose is to print the list of items product codes- PLACEHOLDER, REMOVE WHEN DONE

            db.session.add(new_Order) # This line's purpose is to add the new order to the database
            db.session.commit() # This line's purpose is to commit the new order to the database

            return redirect(url_for('orders')) # This line's purpose is to redirect the user to the list of orders page
        else:
           return render_template('orders_create.html', form=form) # This line's purpose is to render the create order page
    else: # This line's purpose is to check if the current user is not a reseller
        return redirect(url_for('orders')) # This line's purpose is to redirect the user to the list of orders page

#### COMPLETE ####
@app.route('/orders/update_status/<string:order_number>', methods=['GET','POST']) # This line's purpose is to create a new route for the update order page
@login_required
def orders_change_status(order_number):
    """ This function is used to update the status of an order into the database, only admins can update the status of an order"""
    # Admin users must be able to change the status of any order.
    
    # This function is used to change the status of an order 
    # ONLY ADMINS CAN UPDATE THE STATUS OF AN ORDER
    # if the current user is not an admin, redirect to the orders page

    form =  ChangeStatusForm() # This line's purpose is to create a new OrderForm object
    order = Order.query.filter_by(number=order_number).first() # This line's purpose is to get the order from the database
    if order and form.validate_on_submit(): # This line's purpose is to check if the order exists and if the form has been submitted
        order.status = form.status.data # This line's purpose is to update the status of the order
        db.session.commit() # This line's purpose is to commit the updated order to the database
        return redirect(url_for('orders')) # This line's purpose is to redirect the user to the list of orders page
    else:
        return render_template('change_status_order.html', form = form, order = order) # This line's purpose is to render the update order page
    
### THIS IS OPTIONAL, DON'T COMPLETE BEFORE OTHER ROUTES ARE DONE ###  

@app.route('/catalog/<id>/update', methods=['GET','POST']) 
@login_required
def catalog_update(id):
    # The purpose of this function is to update the product catalog 
    form = UpdateOrder()
    return render_template('update_product_catalog.html', form = form)

# This is a helper method to generate the next order number
def generate_order_number(): 
    """ This function is used to generate the order number for a new order"""
    # Get the count of existing orders
    existing_orders_count = Order.query.count()
    # Generate the next order number
    order_number = f"ORD-{str(existing_orders_count + 1).zfill(3)}"
    return order_number # This line's purpose is to return the order number

# This is a helper method to generate the creation date when a new order is created
def generate_create_date():
    """ This function is used to generate the creation date for a new order"""
    # This function is used to generate the creation date
    return datetime.now().strftime("%Y-%m-%d") # This line's purpose is to return the creation date
    
