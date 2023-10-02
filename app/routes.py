'''
CS3250 - Software Development Methods and Tools - Fall 2023
Instructor: Thyago Mota
Student: Joseph Tewolde
Group Name: Backroom Gang
Description: Project01 - Routes for the SQLAlchemy Windoors Web App
'''

from app import app, db, load_user
from app.models import User, Reseller, Admin, Product, Order, Item
from app.forms import SignUpForm, SignInForm, OrderForm, ItemForm, ResellerSignUpForm, AdminSignUpForm
from flask import render_template, redirect, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
import bcrypt

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index(): 
    return render_template('index.html')

@app.route('/users/signin', methods=['GET', 'POST'])
def users_signin():
    #This purpose of this function is to sign in the user by checking if the user exists and if the password is correct 
    form = SignInForm() # This line's purpose is to create a new SignInForm object
    if form.validate_on_submit(): # This line's purpose is to check if the form has been submitted
        user = User.query.filter_by(id=form.id.data).first() # This line's purpose is to check if the user exists
        if user and bcrypt.checkpw(form.passwd.data.encode('utf-8'), user.passwd): # This line's purpose is to check if the password is correct
            login_user(user) # This line's purpose is to sign in the user
            return redirect(url_for('invoices')) # This line's purpose is to redirect the user to the list of users page
    return render_template('users_signin.html', form = form) # This line's purpose is to render the sign in page

@app.route('/register_reseller', methods=['GET', 'POST'])
def register_reseller():
    form = ResellerSignUpForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.passwd.data)
        db.session.add(user)
        db.session.commit()

        reseller = Reseller(user_id=user.id, company=form.company.data, address=form.address.data,
                            phone=form.phone.data, website=form.website.data)
        db.session.add(reseller)
        db.session.commit()

        return redirect(url_for('users_signin'))
    return render_template('reseller_signup.html', form=form)

@app.route('/register_admin', methods=['GET', 'POST'])
def register_admin():
    form = AdminSignUpForm()
    if form.validate_on_submit():
        user = User(id = form.id.data, email=form.email.data, password=form.passwd.data)
        db.session.add(user)
        db.session.commit()

        admin = Admin(userid = user.id, name = form.name.data, title=form.title.data)
        db.session.add(admin)
        db.session.commit()

        return redirect(url_for('users_signin'))
    return render_template('admin_signup.html', form=form)

    
# sign-out functionality from previous homework
@app.route('/users/signout', methods=['GET', 'POST'])
def users_signout():
    logout_user() # this function is used to sign out the user
    return redirect(url_for('index')) # this function is used to redirect the user to the index page

# @app.route('/invoices')
# @login_required
# def invoices():
#     user_invoices = Invoice.query.filter_by(user_id=current_user.id).all() # This line's purpose is to get the list of invoices from the signed-in user (current_user)
#     return render_template('invoices.html', invoices=user_invoices) # This line's purpose is to render the invoices page with the list of invoices from the signed-in user (current_user)

#     #return render_template("invoices.html", user=current_user)

@app.route('/orders')
@login_required
def orders():
    user_orders = Order.query.filter_by(user_id=current_user.id).all() # This line's purpose is to get the list of orders from the signed-in user (current_user)
    return render_template('orders.html', orders=user_orders) # This line's purpose is to render the orders page with the list of orders from the signed-in user (current_user)

# TO-DO #2: get the list of invoices from the signed-in user (current_user); then, create a new invoice with the information gathered from the form and append it to the list of invoices; commit to persist the information into the database
# @app.route('/invoices/create', methods=['GET','POST'])
# @login_required
# def invoices_create():
#     form = InvoiceForm() #Create a new InvoiceForm object
#     if form.validate_on_submit(): # Check if the form has been submitted
#         new_Invoice = Invoice(user_id = current_user.id, number=form.number.data, title=form.title.data, client_name= form.client_name.data, phone_number= form.phone_number.data, due_date=form.due_date.data) # This line's purpose is to create a new invoice with the information gathered from the form
#         db.session.add(new_Invoice) # This line's purpose is to add the new invoice to the database
#         db.session.commit() # This line's purpose is to commit the new invoice to the database
#         return redirect(url_for('invoices')) # This line's purpose is to redirect the user to the list of invoices page
#     else:
#        return render_template('invoices_create.html', form=form) # This line's purpose is to render the create invoice page
    
@app.route('/orders/create', methods=['GET','POST']) # This line's purpose is to create a new route for the create order page
@login_required
def orders_create():
    form = OrderForm() #Create a new OrderForm object
    if form.validate_on_submit(): # Check if the form has been submitted
        new_Order = Order(user_id = current_user.id, number=form.number.data, creation_date=form.creation_date.data, status=form.status.data) # This line's purpose is to create a new order with the information gathered from the form
        db.session.add(new_Order) # This line's purpose is to add the new order to the database
        db.session.commit() # This line's purpose is to commit the new order to the database
        return redirect(url_for('orders')) # This line's purpose is to redirect the user to the list of orders page
    else:
         return render_template('orders_create.html', form=form) # This line's purpose is to render the create order page
    
@app.route('/orders/<id>/update', methods=['GET','POST']) # This line's purpose is to create a new route for the update order page
@login_required
def orders_update(id):
    order = Order.query.filter_by(id=id).first()
    form = OrderForm(obj=order)
    if form.validate_on_submit():
        if current_user == Admin:
            order.number = form.number.data
            order.creation_date = form.creation_date.data
            order.status = form.status.data
            db.session.commit()
        return redirect(url_for('orders'))
    else:
        return render_template('orders_update.html', form=form)

    
