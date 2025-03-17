from flask import Flask, render_template, request, redirect
from datetime import datetime
import json

app = Flask(__name__)

# In-memory storage for orders (resets on server restart)
orders = []

# Define a menu mapping for items
menu = {
    'burger': {'name': 'Burger', 'price': 5},
    'pizza':  {'name': 'Pizza',  'price': 8},
    'soda':   {'name': 'Soda',   'price': 2}
}

# Function to save orders to a JSON file (optional persistence)
def save_orders():
    with open('orders.json', 'w') as f:
        json.dump(orders, f, indent=4)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get selected item keys from the form
        order_keys = request.form.getlist('order')
        
        # Build order details and calculate total price dynamically
        order_details = []
        total_price = 0
        for key in order_keys:
            if key in menu:
                item = menu[key]
                order_details.append(item)
                total_price += item['price']
                
        # Capture customer details
        customer_name = request.form.get('customer_name')
        location = request.form.get('location')
        
        # Create a new order with a unique ID, timestamp, and status
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
        save_orders()  # Optional: persist orders to a JSON file
        
        # Render the confirmation page with order details
        return render_template('confirmation.html',
                               customer_name=customer_name,
                               location=location,
                               order=order_details,
                               total_price=total_price)
    return render_template('index.html')

# Admin dashboard to view all orders
@app.route('/admin')
def admin():
    return render_template('admin.html', orders=orders)

# Route to update an order's status
@app.route('/update_status/<int:order_id>/<status>')
def update_status(order_id, status):
    for order in orders:
        if order['order_id'] == order_id:
            order['status'] = status
            break
    save_orders()  # Optional: update persistence
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)
