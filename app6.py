from flask import Flask, render_template, request
from datetime import datetime
import json

app = Flask(__name__)

# In-memory storage for orders (will reset on server restart)
orders = []

# Define a menu mapping for item keys to their details
menu = {
    'burger': {'name': 'Burger', 'price': 5},
    'pizza':  {'name': 'Pizza',  'price': 8},
    'soda':   {'name': 'Soda',   'price': 2}
}

# Function to save orders to a JSON file (optional enhancement)
def save_orders():
    with open('orders.json', 'w') as f:
        json.dump(orders, f, indent=4)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get selected item keys from the form
        order_keys = request.form.getlist('order')
        
        # Build order details and calculate total dynamically
        order_details = []
        total_price = 0
        for key in order_keys:
            if key in menu:
                item = menu[key]
                order_details.append(item)
                total_price += item['price']
        
        # Capture Customer Details
        customer_name = request.form.get('customer_name')
        location = request.form.get('location')
        
        # Create a new order with a timestamp
        new_order = {
            'customer_name': customer_name,
            'location': location,
            'order': order_details,
            'total_price': total_price,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        orders.append(new_order)
        save_orders()  # Optional: save to JSON file
        
        # Render the confirmation page, passing the computed total and order details
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

if __name__ == '__main__':
    app.run(debug=True)
