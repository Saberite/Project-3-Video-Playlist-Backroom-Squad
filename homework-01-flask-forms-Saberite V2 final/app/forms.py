'''
CS3250 - Software Development Methods and Tools - Fall 2023
Instructor: Thyago Mota
Student: Bryan Thao
Description: Homework 01 - Forms for the Invoices Web App
'''

from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, DateField, SubmitField, validators
from wtforms.validators import DataRequired

# TODO #2: complete the invoice form with the missing fields (title, client name, phone number, and due date)
class InvoiceForm(FlaskForm):
    number = StringField('Invoice#', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    client_name = StringField('Client Name', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    due_date = DateField('Due Date', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
