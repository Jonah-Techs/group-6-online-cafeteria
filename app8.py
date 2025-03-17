from flask import Flask, render_template, request, redirect
from datetime import datetime
import os
import json

app = Flask(__name__)

# Load orders from orders.json if available; otherwise, initialize as empty list
if os.path.exists('orders.json'):
    with open('orders.json', 'r') as f:
        orders = json.load(f)
else:
    orders = []

# Define a menu mapping for items
menu = {
    'burger': {'name': 'Burger', 'price': 5000},
    'pizza':  {'name': 'Pizza',  'price': 8000},
    'soda':   {'name': 'Soda',   'price': 2000},
    'embori': {'name': 'embori', 'price': 20000},
    'envuruga': {'name': 'envuruga', 'price': 9000}
}

# Function to save orders to a JSON file
def save_orders():
    with open('orders.json', 'w') as f:
        json.dump(orders, f, indent=4)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        order_keys = request.form.getlist('order')
        order_details = []
        total_price = 0
        for key in order_keys:
            if key in menu:
                item = menu[key]
                order_details.append(item)
                total_price += item['price']

        customer_name = request.form.get('customer_name')
        location = request.form.get('location')
        
        new_order = {
            'order_id': len(orders) + 1,
            'customer_name': customer_name,
            'location': location,
            'order': order_details,
            'total_price': total_price,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'status': 'Pending'
        }
        orders.append(new_order)
        save_orders()  # Persist the new order
        
        return render_template('confirmation.html',
                               customer_name=customer_name,
                               location=location,
                               order=order_details,
                               total_price=total_price)
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html', orders=orders)

@app.route('/update_status/<int:order_id>/<status>')
def update_status(order_id, status):
    for order in orders:
        if order['order_id'] == order_id:
            order['status'] = status
            break
    save_orders()  # Persist the status update
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)
