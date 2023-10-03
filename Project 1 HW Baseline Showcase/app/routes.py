'''
CS3250 - Software Development Methods and Tools - Fall 2023
Instructor: Thyago Mota
Group: Backroom Gang
Group Project 1: Windoors
'''

from app import app
from flask import render_template, redirect, url_for, request, session
from app.forms import InvoiceForm

@app.route('/')
@app.route('/invoices')
@app.route('/index.html')

#Welcome page for sign in and sign out
def welcome_page():
    return render_template("welcome.html") 

#Redirect from sign in to index.html
@app.route('/list_invoices') 
def list_invoices():
    return render_template("index.html", title=app.config['TITLE'], invoices=app.config['INVOICES']) #Index is the Order Table

#We will have to create seperate pages for Products, Order, Items potenitally?
#Left create_invoices as is for example purposes
@app.route('/invoices/create', methods=['GET','POST'])
def create_invoice():
    form = InvoiceForm()
    if form.validate_on_submit(): 
        app.config['INVOICES'].append(
            { 'number': form.number.data, 
              'title': form.title.data, 
              'client_name': form.client_name.data, 
              'phone_number': form.phone_number.data, 
              'due_date': form.due_date.data }
        ) 
        return redirect(url_for('list_invoices'))
    else:
       return render_template('invoices_create.html', title=app.config['TITLE'], form=form)



#Test User and password. It's test and test for both user and password. Replace with SQLalchemy here!
user = {
        'test': 'test',
        }

#Test Login code. Courtesy of ChatGpt!
@app.route('/test_sign_in', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in user and user[username] == password:
            session['logged_in'] = True
            return redirect('/list_invoices')
        else:
            return 'Invalid username or password'
    return render_template('test_sign_in.html')