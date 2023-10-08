'''
CS3250 - Software Development Methods and Tools - Fall 2023
Instructor: Thyago Mota
Group: Backroom Gang
Description: Project 01 - Windoors
'''

from flask import Flask

app = Flask("Authentication Web App")
app.config['SECRET_KEY']  = 'you-will-never-guess'

# initial admin user for Professor Mota
app.config['Initial_Admin'] = [
    {'id': 'tmota', 'email': 'tmota@msudenver.edu', 'passwd': '1', 'creation_date': '2021-09-01', 'role': 'admin', 'name': 'Thyago Mota', 'title': 'Professor'}
]

app.config['INITIAL_PRODUCTS'] = [
    {'product_code': 'door-001', 'quantity': 0, 'specs': ''},  # This is the initial product list
    {'product_code': 'door-002', 'quantity': 0, 'specs': ''}, 
    {'product_code': 'window-001', 'quantity': 0, 'specs': ''},
]


# db initialization
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.init_app(app)

from app import models
from app import tMotaAdmin
with app.app_context(): 
    db.create_all()
    tMotaAdmin.create_admin() # create initial admin user

# login manager
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

from app.models import User

# user_loader callback
@login_manager.user_loader
def load_user(id):
    try: 
        return db.session.query(User).filter(User.id==id).one()
    except: 
        return None

from app import routes