'''
CS3250 - Software Development Methods and Tools - Fall 2023
Instructor: Thyago Mota
Group: Backroom Gang
Group Project 1: Windoors
'''

from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, DateField, SubmitField, TextAreaField, PasswordField, validators
from wtforms.validators import DataRequired

#InvoiceForm is a general idea of what each class will need. Only changes here was title of each field for showcase purposes.
class InvoiceForm(FlaskForm):
    number = StringField('Product', validators=[DataRequired()])
    title = StringField('Description', validators=[DataRequired()])
    client_name = StringField('Type', validators=[DataRequired()])
    phone_number = StringField('Available?', validators=[DataRequired()])
    due_date = StringField('Extra? Company?', validators=[DataRequired()])
    submit = SubmitField('Submit')

#Test Class for product. Order/Items/product will need classes   
class ProductForm(FlaskForm):
    code = StringField('Invoice#', validators=[DataRequired()])
    description = StringField('Title', validators=[DataRequired()])
    type = StringField('Client Name', validators=[DataRequired()])
    available = StringField('Phone Number', validators=[DataRequired()])
    price = StringField('Due Date', validators=[DataRequired()])
    submit = SubmitField('Submit')

#Test for OrderFrom
class OrderForm(FlaskForm):
    order_number = StringField('Order #', validators=[DataRequired()])
    creation_date = StringField('Creation Date', validators=[DataRequired()])
    status = StringField('Status(True/False)', validators=[DataRequired()])
    submit = SubmitField('Submit')

#Test for ItemForm
class ItemForm(FlaskForm):
    order_id = StringField('Order Number', validators=[DataRequired()])
    sequetial_id = StringField('Sequetial Number', validators=[DataRequired()])
    product_code = StringField('Product Code', validators=[DataRequired()])
    quantiy = StringField('Qty', validators=[DataRequired()])
    specs = StringField('Specs', validators=[DataRequired()])
    submit = SubmitField('Submit')
    

#SignUpForm and SignInForms will below here when we start coding!
