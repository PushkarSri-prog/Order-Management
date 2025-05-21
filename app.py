from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask import jsonify
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'freight_management'
mysql = MySQL(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT user_id, username, password FROM users WHERE username=%s AND password=%s", (username, password))
        user = cur.fetchone()
        cur.close()
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

# Home route
@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Dashboard
@app.route('/dashboard')
def dashboard():
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM job_order")
    job_orders = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM pickup_acceptance")
    pickups = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM pod")
    pods = cur.fetchone()[0]
    cur.close()
    return render_template('dashboard.html', job_orders=job_orders, pickups=pickups, pods=pods)

# Country Master
@app.route('/country', methods=['GET', 'POST'])
def country_master():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        country_name = request.form['country_name']
        cur.execute("INSERT INTO country (country_name) VALUES (%s)", (country_name,))
        mysql.connection.commit()
        return redirect(url_for('country_master'))
    cur.execute("SELECT * FROM country")
    countries = cur.fetchall()
    cur.close()
    return render_template('country.html', countries=countries)

# State Master
@app.route('/state', methods=['GET', 'POST'])
def state_master():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM country")
    countries = cur.fetchall()
    if request.method == 'POST':
        state_name = request.form['state_name']
        country_id = request.form['country_id']
        cur.execute("INSERT INTO state (state_name, country_id) VALUES (%s, %s)", (state_name, country_id))
        mysql.connection.commit()
        return redirect(url_for('state_master'))
    cur.execute("""
        SELECT state.state_id, state.state_name, country.country_name
        FROM state
        JOIN country ON state.country_id = country.country_id
    """)
    states = cur.fetchall()
    cur.close()
    return render_template('state.html', states=states, countries=countries)

# City Master
@app.route('/city', methods=['GET', 'POST'])
def city_master():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM country")
    countries = cur.fetchall()
    cur.execute("SELECT state.state_id, state.state_name, country.country_id, country.country_name FROM state JOIN country ON state.country_id = country.country_id")
    states = cur.fetchall()
    if request.method == 'POST':
        city_name = request.form['city_name']
        state_id = request.form['state_id']
        cur.execute("INSERT INTO city (city_name, state_id) VALUES (%s, %s)", (city_name, state_id))
        mysql.connection.commit()
        return redirect(url_for('city_master'))
    cur.execute("""
        SELECT city.city_id, city.city_name, state.state_name, country.country_name
        FROM city
        JOIN state ON city.state_id = state.state_id
        JOIN country ON state.country_id = country.country_id
    """)
    cities = cur.fetchall()
    cur.close()
    return render_template('city.html', cities=cities, countries=countries, states=states)

# Customer Master
@app.route('/customer', methods=['GET', 'POST'])
def customer_master():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM country")
    countries = cur.fetchall()
    cur.execute("SELECT * FROM state")
    states = cur.fetchall()
    cur.execute("SELECT * FROM city")
    cities = cur.fetchall()
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        contact_person = request.form['contact_person']
        contact_number = request.form['contact_number']
        email = request.form['email']
        address = request.form['address']
        country_id = request.form['country_id']
        state_id = request.form['state_id']
        city_id = request.form['city_id']
        cur.execute("""
            INSERT INTO customer (customer_name, contact_person, contact_number, email, address, city_id, state_id, country_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (customer_name, contact_person, contact_number, email, address, city_id, state_id, country_id))
        mysql.connection.commit()
        return redirect(url_for('customer_master'))
    cur.execute("""
        SELECT customer.customer_id, customer.customer_name, customer.contact_person, customer.contact_number, customer.email, customer.address,
               city.city_name, state.state_name, country.country_name
        FROM customer
        LEFT JOIN city ON customer.city_id = city.city_id
        LEFT JOIN state ON customer.state_id = state.state_id
        LEFT JOIN country ON customer.country_id = country.country_id
    """)
    customers = cur.fetchall()
    cur.close()
    return render_template('customer.html', customers=customers, countries=countries, states=states, cities=cities)

# Transporter Master
@app.route('/transporter', methods=['GET', 'POST'])
def transporter_master():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM country")
    countries = cur.fetchall()
    cur.execute("SELECT * FROM state")
    states = cur.fetchall()
    cur.execute("SELECT * FROM city")
    cities = cur.fetchall()
    if request.method == 'POST':
        transporter_name = request.form['transporter_name']
        contact_person = request.form['contact_person']
        contact_number = request.form['contact_number']
        email = request.form['email']
        address = request.form['address']
        country_id = request.form['country_id']
        state_id = request.form['state_id']
        city_id = request.form['city_id']
        cur.execute("""
            INSERT INTO transporter (transporter_name, contact_person, contact_number, email, address, city_id, state_id, country_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (transporter_name, contact_person, contact_number, email, address, city_id, state_id, country_id))
        mysql.connection.commit()
        return redirect(url_for('transporter_master'))
    cur.execute("""
        SELECT transporter.transporter_id, transporter.transporter_name, transporter.contact_person, transporter.contact_number, transporter.email, transporter.address,
               city.city_name, state.state_name, country.country_name
        FROM transporter
        LEFT JOIN city ON transporter.city_id = city.city_id
        LEFT JOIN state ON transporter.state_id = state.state_id
        LEFT JOIN country ON transporter.country_id = country.country_id
    """)
    transporters = cur.fetchall()
    cur.close()
    return render_template('transporter.html', transporters=transporters, countries=countries, states=states, cities=cities)

# Item Master
@app.route('/item', methods=['GET', 'POST'])
def item_master():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        item_name = request.form['item_name']
        item_description = request.form['item_description']
        item_code = request.form['item_code']
        cur.execute("""
            INSERT INTO item (item_name, item_description, item_code)
            VALUES (%s, %s, %s)
        """, (item_name, item_description, item_code))
        mysql.connection.commit()
        return redirect(url_for('item_master'))
    cur.execute("SELECT * FROM item")
    items = cur.fetchall()
    cur.close()
    return render_template('item.html', items=items)

@app.route('/job_order', methods=['GET', 'POST'])
def job_order():
    cur = mysql.connection.cursor()
    # Fetch dropdown data
    cur.execute("SELECT * FROM customer")
    customers = cur.fetchall()
    cur.execute("SELECT * FROM transporter")
    transporters = cur.fetchall()
    cur.execute("SELECT * FROM city")
    cities = cur.fetchall()
    cur.execute("SELECT * FROM item")
    items = cur.fetchall()

    if request.method == 'POST':
        job_order_number = request.form['job_order_number']
        customer_id = request.form['customer_id']
        transporter_id = request.form['transporter_id']
        origin_city_id = request.form['origin_city_id']
        destination_city_id = request.form['destination_city_id']
        order_date = request.form['order_date']
        status = request.form['status']
        remarks = request.form.get('remarks', '')

        # Insert job order
        cur.execute("""
            INSERT INTO job_order (job_order_number, customer_id, transporter_id, origin_city_id, destination_city_id, order_date, status, remarks)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (job_order_number, customer_id, transporter_id, origin_city_id, destination_city_id, order_date, status, remarks))
        mysql.connection.commit()
        job_order_id = cur.lastrowid

        # Insert job order items
        item_ids = request.form.getlist('item_id')
        quantities = request.form.getlist('quantity')
        for item_id, qty in zip(item_ids, quantities):
            if item_id and qty:
                cur.execute("""
                    INSERT INTO job_order_item (job_order_id, item_id, quantity)
                    VALUES (%s, %s, %s)
                """, (job_order_id, item_id, qty))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('job_order'))

    else:
        cur.execute("""
            SELECT jo.job_order_id, jo.job_order_number, c.customer_name, t.transporter_name,
                   oc.city_name AS origin_city, dc.city_name AS dest_city,
                   jo.order_date, jo.status, jo.remarks
            FROM job_order jo
            JOIN customer c ON jo.customer_id = c.customer_id
            JOIN transporter t ON jo.transporter_id = t.transporter_id
            JOIN city oc ON jo.origin_city_id = oc.city_id
            JOIN city dc ON jo.destination_city_id = dc.city_id
            ORDER BY jo.job_order_id DESC
        """)
        job_orders = cur.fetchall()
        cur.close()
        return render_template('job_order.html', job_orders=job_orders, customers=customers, transporters=transporters, cities=cities, items=items)

@app.route('/pickup_acceptance', methods=['GET', 'POST'])
def pickup_acceptance():
    cur = mysql.connection.cursor()
    # Fetch job orders for dropdown
    cur.execute("SELECT job_order_id, job_order_number FROM job_order ORDER BY job_order_id DESC")
    job_orders = cur.fetchall()

    if request.method == 'POST':
        job_order_id = request.form['job_order_id']
        pickup_date = request.form['pickup_date']
        accepted_by = request.form['accepted_by']
        remarks = request.form.get('remarks', '')

        # Insert into pickup_acceptance
        cur.execute("""
            INSERT INTO pickup_acceptance (job_order_id, pickup_date, accepted_by, remarks)
            VALUES (%s, %s, %s, %s)
        """, (job_order_id, pickup_date, accepted_by, remarks))
        mysql.connection.commit()

        # --- Update job_order status to 'Pickup done' ---
        cur.execute("""
            UPDATE job_order SET status=%s WHERE job_order_id=%s
        """, ("Pickup done", job_order_id))
        mysql.connection.commit()

        cur.close()
        return redirect(url_for('pickup_acceptance'))
    else:
        cur.execute("""
            SELECT pa.pickup_id, jo.job_order_number, pa.pickup_date, pa.accepted_by, pa.remarks
            FROM pickup_acceptance pa
            JOIN job_order jo ON pa.job_order_id = jo.job_order_id
            ORDER BY pa.pickup_id DESC
        """)
        pickups = cur.fetchall()
        cur.close()
        return render_template('pickup_acceptance.html', pickups=pickups, job_orders=job_orders)

# POD - Uses delivery_date as per your schema
@app.route('/pod', methods=['GET', 'POST'])
def pod():
    cur = mysql.connection.cursor()
    # Fetch job orders for the dropdown
    cur.execute("""
        SELECT job_order_id, job_order_number 
        FROM job_order 
        ORDER BY job_order_id DESC
    """)
    job_orders = cur.fetchall()
    
    # Fetch all saved PODs with job order info, using correct column names
    cur.execute("""
        SELECT 
            p.pod_id, 
            jo.job_order_number, 
            p.delivery_date, 
            p.received_by, 
            p.remarks, 
            p.pod_document
        FROM pod p
        JOIN job_order jo ON p.job_order_id = jo.job_order_id
        ORDER BY p.pod_id DESC
    """)
    pods = cur.fetchall()
    cur.close()
    return render_template('pod.html', job_orders=job_orders, pods=pods)

# MIS Job Orders
@app.route('/mis/job_orders')
def mis_job_orders():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("""
        SELECT
            jo.job_order_id,
            jo.job_order_number,
            c.customer_name AS customer,
            t.transporter_name AS transporter,
            oc.city_name AS origin_city,
            dc.city_name AS destination_city,
            jo.order_date,
            jo.status,
            jo.remarks
        FROM job_order jo
        LEFT JOIN customer c ON jo.customer_id = c.customer_id
        LEFT JOIN transporter t ON jo.transporter_id = t.transporter_id
        LEFT JOIN city oc ON jo.origin_city_id = oc.city_id
        LEFT JOIN city dc ON jo.destination_city_id = dc.city_id
        ORDER BY jo.job_order_id DESC
    """)
    job_orders = cur.fetchall()
    cur.close()
    return render_template('mis_job_orders.html', job_orders=job_orders)

# MIS PODs
@app.route('/mis/pod')
def mis_pod():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("""
        SELECT
            p.pod_id,
            p.received_by,
            p.remarks,
            jo.job_order_number,
            c.customer_name AS customer
        FROM pod p
        LEFT JOIN job_order jo ON p.job_order_id = jo.job_order_id
        LEFT JOIN customer c ON jo.customer_id = c.customer_id
        ORDER BY p.pod_id DESC
    """)
    pods = cur.fetchall()
    cur.close()
    return render_template('mis_pod.html', pods=pods)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/dashboard_counts')
def api_dashboard_counts():
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM job_order")
    job_orders = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM pickup_acceptance")
    pickups = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM pod")
    pods = cur.fetchone()[0]
    cur.close()
    return jsonify({'job_orders': job_orders, 'pickups': pickups, 'pods': pods})

# --- API: Create Job Order (for AJAX) ---
@app.route('/api/job_order', methods=['POST'])
def api_create_job_order():
    data = request.json
    cur = mysql.connection.cursor()
    # Insert job order
    cur.execute("""
        INSERT INTO job_order (job_order_number, customer_id, transporter_id, origin_city_id, destination_city_id, order_date, status, remarks)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data['job_order_number'], data['customer_id'], data['transporter_id'],
        data['origin_city_id'], data['destination_city_id'], data['order_date'],
        data['status'], data.get('remarks', '')
    ))
    mysql.connection.commit()
    job_order_id = cur.lastrowid
    # Insert items if present
    for item in data.get('items', []):
        cur.execute("""
            INSERT INTO job_order_item (job_order_id, item_id, quantity)
            VALUES (%s, %s, %s)
        """, (job_order_id, item['item_id'], item['quantity']))
    mysql.connection.commit()
    cur.close()
    return jsonify({'status': 'success', 'job_order_id': job_order_id})

# --- API: Create Pickup (for AJAX) ---
@app.route('/api/pickup', methods=['POST'])
def api_create_pickup():
    data = request.json
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO pickup_acceptance (job_order_id, pickup_date, accepted_by, remarks)
        VALUES (%s, %s, %s, %s)
    """, (
        data['job_order_id'], data['pickup_date'], data['accepted_by'], data.get('remarks', '')
    ))
    mysql.connection.commit()
    pickup_id = cur.lastrowid

    # --- Update job_order status to 'Pickup done' ---
    cur.execute("""
        UPDATE job_order SET status=%s WHERE job_order_id=%s
    """, ("Pickup done", data['job_order_id']))
    mysql.connection.commit()

    cur.close()
    return jsonify({'status': 'success', 'pickup_id': pickup_id})

# --- API: Create POD (for AJAX) ---
@app.route('/api/pod', methods=['POST'])
def api_create_pod():
    data = request.json
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO pod (job_order_id, delivery_date, received_by, remarks)
        VALUES (%s, %s, %s, %s)
    """, (
        data['job_order_id'], data['delivery_date'], data['received_by'], data.get('remarks', '')
    ))
    mysql.connection.commit()
    pod_id = cur.lastrowid
    cur.close()
    return jsonify({'status': 'success', 'pod_id': pod_id})

# Add your other transaction and MIS routes here, without login/session logic

if __name__ == '__main__':
    app.run(debug=True)