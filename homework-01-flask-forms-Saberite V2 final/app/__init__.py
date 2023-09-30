'''
CS3250 - Software Development Methods and Tools - Fall 2023
Instructor: Thyago Mota
Student: Bryan Thao
Description: Homework 01 - Invoices Web App
'''

from flask import Flask

app = Flask(__name__)

# global configuration parameters 
# consider using ENVIRONMENT VARIABLES to improve security
app.config['SECRET_KEY']  = 'you-will-never-guess'
app.config['TITLE']       = 'Invoices Web App'
app.config['INVOICES'] = [
    { 'number': 'INV-d51t', 'title': 'Marketing Plan for Product XYZ', 'client_name': 'Donna Summmers', 'phone_number': '(303) 741-3409', 'due_date': '06/01/23'}, 
    { 'number': 'INV-49f9', 'title': 'Training for the Developing Team', 'client_name': 'Jayson Brown', 'phone_number': '(707) 322-2435', 'due_date': '01/08/23'}, 
    { 'number': 'INV-881q', 'title': 'Pizza for the Cloud Computing Event', 'client_name': 'Sam Tyron', 'phone_number': '(484) 345-3322', 'due_date': '09/08/23'}
]

from app import routes