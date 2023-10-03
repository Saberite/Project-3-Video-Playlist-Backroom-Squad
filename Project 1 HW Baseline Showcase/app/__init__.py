'''
CS3250 - Software Development Methods and Tools - Fall 2023
Instructor: Thyago Mota
Group: Backroom Gang
Group Project 1: Windoors
'''

from flask import Flask

app = Flask(__name__)

# global configuration parameters 
# consider using ENVIRONMENT VARIABLES to improve security
app.config['SECRET_KEY']  = 'you-will-never-guess'
app.config['TITLE']       = 'Invoices Web App'
app.config['INVOICES'] = [
    { 'number': 'Product', 'title': 'Order#', 'client_name': 'Item', 'phone_number': 'Extra? Company?', 'due_date': 'Extra'}, 
    { 'number': 'Product', 'title': 'Order#', 'client_name': 'Item', 'phone_number': 'Extra? Company?', 'due_date': 'Extra'}, 
    { 'number': 'Product', 'title': 'Order#', 'client_name': 'Item', 'phone_number': 'Extra? Company?', 'due_date': 'Extra'}
]

from app import routes