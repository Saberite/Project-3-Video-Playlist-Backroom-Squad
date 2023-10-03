'''
CS3250 - Software Development Methods and Tools - Fall 2023
Instructor: Thyago Mota
Student: Joseph Tewolde
Group Name: Backroom Gang
Description: Project 01 - Forms for Windoors Web App
'''

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, validators, FormField, FieldList, EmailField
from wtforms.validators import DataRequired

class SignUpForm(FlaskForm):
    id = StringField('Id', validators=[DataRequired()]) 
    email = StringField('Email', validators=[DataRequired()])
    creation_date = DateField('Creation Date', validators=[DataRequired()])
    passwd = PasswordField('Password', validators=[DataRequired()])
    passwd_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Confirm')

class ResellerSignUpForm(SignUpForm):
    company = StringField('Company', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    website = StringField('Website', validators=[DataRequired()])

class AdminSignUpForm(SignUpForm):
    name = StringField('Name', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])


class SignInForm(FlaskForm):
    id = StringField('Id', validators=[DataRequired()])
    passwd = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Confirm')

class ItemForm(FlaskForm):
    product_code = StringField('Product Code', validators=[DataRequired()])
    quantity = StringField('Quantity', validators=[DataRequired()])
    specs = StringField('Specs', validators=[DataRequired()])
    
class OrderForm(FlaskForm):
    number = StringField('Order#', validators=[DataRequired()])
    creation_date = StringField('Creation Date', validators=[DataRequired()])
    status = StringField('Status', validators=[DataRequired()])
    items = FieldList(FormField(ItemForm), min_entries=1)
    submit = SubmitField('Confirm')
