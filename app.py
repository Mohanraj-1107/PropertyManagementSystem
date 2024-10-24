from flask import Flask, render_template,request,Response,flash,redirect,url_for,session
import sqlite3 
import os
from flask import make_response
app = Flask(__name__)
app.secret_key = "Mohanraj"


def get_db_connection():
    conn = sqlite3.connect('rental_management.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('Home.html');

@app.route("/Login",methods=['POST'])
def login():
    user_type = request.form['userType']  
    username = request.form['loginUsername']  
    password = request.form['loginPassword']  
    conn = get_db_connection()
    
    if user_type == 'owner':
        query = 'SELECT * FROM owner WHERE username = ? AND password = ?'
        user=conn.execute(query, (username, password)).fetchone()
        if user:
             session['username'] = username
             session['role']=user_type
             username = session.get('username', 'Guest') 
             return render_template('owner.html',username=username)
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('home'))  
    
    elif user_type == 'Admin':
        if username=='Admin' and password=='Admin@2024':
             session['username'] = username
             session['role']=user_type
             username = session.get('username', 'Guest')
             return render_template('Admin.html',username="Admin")
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('home'))
    
    elif user_type=='tenant':  
        query = 'SELECT * FROM tenant WHERE username = ? AND password = ?'
        user=conn.execute(query, (username, password)).fetchone()
        if user:
             session['username'] = username
             session['role']=user_type
             username = session.get('username', 'Guest')
             return render_template('Tenant.html',username=username)
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('home'))
    else:
        flash('Invalid username or password', 'danger')
        return redirect(url_for('home'))  
    
@app.route('/signup', methods=['POST'])
def signup():
    user_type = request.form['signupUserType']
    username = request.form['signupUsername']
    email = request.form['signupEmail']
    password = request.form['signupPassword']
    confirm_password = request.form['signupConfirmPassword']

    if password == confirm_password:
        insert_user(user_type, username, email, password)
        return redirect(url_for('home'))
    else:
        return "Passwords do not match", 400
   
def insert_user(user_type, username, email, password):
    conn = sqlite3.connect('rental_management.db')
    cursor = conn.cursor()

    if user_type == "owner":
        cursor.execute("INSERT INTO owner (username, email, password) VALUES (?, ?, ?)", (username, email, password))
    elif user_type == "admin":
        cursor.execute("INSERT INTO admin (username, email, password) VALUES (?, ?, ?)", (username, email, password))
    else: 
        cursor.execute("INSERT INTO tenant (username, email, password) VALUES (?, ?, ?)", (username, email, password))

    conn.commit()
    conn.close()

@app.route("/Logout")
def Logout():
    return redirect(url_for('home'))

@app.route("/postproperties")
def posting():
    return render_template('Details.html');

@app.route('/returnHome')
def returnHome():
    if 'role' in session:
        if session['role'] == 'Admin':
            return redirect(url_for('admin_home'))
        elif session['role'] == 'owner':
            return redirect(url_for('owner_home'))
        elif session['role']=='tenant':
            return redirect(url_for('Tenant_home'))
    else:
        return redirect(url_for('login'))

@app.route('/admin_home')
def admin_home():
    return render_template('Admin.html', username=session.get('username'))

@app.route('/owner_home')
def owner_home():
    return render_template('owner.html', username=session.get('username'))

@app.route('/Tenant_home')
def Tenant_home():
    return render_template('Tenant.html', username=session.get('username'))

def insert_property(title, description, address, price, property_type, contact_number):
    conn = sqlite3.connect('rental_management.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO properties (title, description, address, price, type, contact_number)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (title, description, address, price, property_type, contact_number))
    conn.commit()
    conn.close()

@app.route('/submit_property', methods=['POST'])
def submit_property():
    title = request.form['propertyTitle']
    description = request.form['propertyDescription']
    address = request.form['propertyAddress']
    price = request.form['propertyPrice']
    property_type = request.form['propertyType']
    contact_number = request.form['contactNumber']

    try:
        insert_property(title, description, address, price, property_type, contact_number)
        flash('Property submitted successfully!', 'success')
    except Exception as e:
        flash('Error submitting property: ' + str(e), 'danger')

    return redirect(url_for('properties'))


@app.route('/property_form')
def properties():
    conn = get_db_connection()
    properties = conn.execute('SELECT * FROM properties').fetchall()  
    conn.close()
    return render_template('propertyview.html', properties=properties) 

@app.route('/update_property', methods=['POST'])
def update_property():
    property_id = request.form.get('propertyId')
    title = request.form.get('title')
    location = request.form.get('location')
    contact_number = request.form.get('contact_number')
    price = request.form.get('price')
    description = request.form.get('description')

    print(f'Updating property: {property_id}, Title: {title}, Location: {location}, Contact: {contact_number}, Price: {price}, Description: {description}')

    conn = get_db_connection()
    conn.execute('''
            UPDATE properties
            SET title = ?, address = ?, contact_number = ?, price = ?, description = ?
            WHERE id = ?
        ''', (title, location, contact_number, float(price), description, property_id))
    conn.commit()
    flash('Property updated successfully!', 'success')
    conn.close()
    return redirect(url_for('properties'))

@app.route('/delete_property/<int:id>', methods=['GET'])
def delete_property(id):
    conn = get_db_connection()
    try:
        property = conn.execute('SELECT * FROM properties WHERE id = ?', (id,)).fetchone()
        if property is None:
            flash('Property not found!', 'danger')
            return redirect(url_for('property_view'))
        conn.execute('DELETE FROM properties WHERE id = ?', (id,))
        conn.commit()

    except Exception as e:
        conn.rollback()

    finally:
        conn.close()

    return redirect(url_for('properties'))

@app.route('/admin/owners')
def view_owners():
    conn = get_db_connection()
    owners = conn.execute('SELECT * FROM owner').fetchall()
    conn.close()
    return render_template('owners.html', owners=owners)

@app.route('/admin/tenants')
def view_tenants():
    conn = get_db_connection()
    tenants = conn.execute('SELECT * FROM tenant').fetchall()
    conn.close()
    return render_template('tenants.html', tenants=tenants)

@app.route("/propertyview")
def propertyview():
    conn = get_db_connection()
    properties = conn.execute('SELECT * FROM properties').fetchall()  
    conn.close()
    return render_template('TenantsProperty.html', properties=properties) 

@app.route('/book_property', methods=['POST'])
def book_property():
    tenant_name = request.form.get('tenant_name')
    tenant_email = request.form.get('tenant_email')
    tenant_phone = request.form.get('tenant_phone')
    property_id = request.form.get('property_id')  
    if not property_id:
        flash('Invalid property. Please try again.', 'danger')
        return redirect(url_for('properties'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO bookings (tenant_name, tenant_email, tenant_phone, property_id)
        VALUES (?, ?, ?, ?)
    ''', (tenant_name, tenant_email, tenant_phone, property_id))
    
    cursor.execute('''
        UPDATE properties
        SET is_booked = 1
        WHERE id = ?
    ''', (property_id,))
    
    conn.commit()
    conn.close()
    flash('Property booked successfully!', 'success')
    return redirect(url_for('propertyview'))

@app.route('/admin/Bookings')
def view_bookings():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT bookings.tenant_name, bookings.tenant_email, bookings.tenant_phone,
               properties.title, properties.address
        FROM bookings
        JOIN properties ON bookings.property_id = properties.id
    ''')
    bookings = cursor.fetchall()
    conn.close()
    return render_template('view_Bookings.html', bookings=bookings)

if __name__ == '__main__':
    app.run(debug=True)
