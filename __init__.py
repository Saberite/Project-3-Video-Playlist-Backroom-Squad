'''
CS3250 - Software Development Methods and Tools - Fall 2023
Instructor: Thyago Mota
Group: Backroom Gang
Description: Project 01 - Windoors
'''

from flask import Flask

app = Flask("Authentication Web App")
app.config['SECRET_KEY']  = 'you-will-never-guess'


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
with app.app_context(): 
    db.create_all()

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