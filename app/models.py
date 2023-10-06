'''
CS3250 - Software Development Methods and Tools - Fall 2023
Project 01- Windoors
Description: This program is meant for implementing the data model with Flask
Group Name: Backroom Gang
Developed by: Joseph Tewolde
'''

# These are the imports for the program
from app import db
from flask_login import UserMixin

# This is the User class for the program
class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.String, primary_key=True) # user id
    email = db.Column(db.String, unique=True, nullable=False) # email address
    passwd = db.Column(db.String) # password 
    creation_date = db.Column(db.String) # date of creation

# This is the ResellerUser class for the program
class Reseller(User):
    __tablename__ = "resellers"
    id = db.Column(db.String, db.ForeignKey("users.id"), primary_key=True) # user id
    company = db.Column(db.String()) # company name
    address = db.Column(db.String()) # company address
    phone = db.Column(db.String()) # company phone number
    website = db.Column(db.String()) # company website
    orders = db.relationship("Order", cascade="delete") # reseller orders 

# This is the AdminUser class for the program
class Admin(User):
    __tablename__ = "admins"
    id = db.Column(db.String, db.ForeignKey("users.id"), primary_key=True) # user id
    name = db.Column(db.String()) # admin name
    title = db.Column(db.String()) # admin title

# This is the Product class for the program
class Product(db.Model):
    __tablename__ = "products"
    code = db.Column(db.String, primary_key=True) # product code
    description = db.Column(db.String) # product description
    type = db.Column(db.String) # product type
    available = db.Column(db.Boolean) # product availability
    price = db.Column(db.Float) # product price

# This is the Order class for the program
class Order(db.Model):
    __tablename__ = "orders" 

    number = db.Column(db.String(), primary_key=True) # order number
    creation_date = db.Column(db.String()) # order creation date
    status = db.Column(db.String()) # order status

    # Establish a one-to-many relationship between Order and Items
    items = db.relationship("Item", cascade="delete") # order items

    # Establish a many-to-one relationship between Order and Users
    reseller_id = db.Column(db.String, db.ForeignKey("resellers.id"), primary_key = True) # user id

# This is the Item class for the program
class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.String, primary_key=True) # item id
    order_number = db.Column(db.String, db.ForeignKey("orders.number")) # order number
    sequential_number = db.Column(db.Integer) # item sequential number
    product_code = db.Column(db.String, db.ForeignKey("products.code")) # product code
    quantity = db.Column(db.Integer) # item quantity
    specs = db.Column(db.String) # item specifications

    # Establish a one-to-one relationship between Items and Products
    product = db.relationship("Product") # item product

    # Establish a many-to-one relationship between Items and Orders
    order = db.relationship("Order", overlaps="items") # item order
