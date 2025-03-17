from flask import Flask, render_template, request
from datetime import datetime
import json

app = Flask(__name__)

# In-memory storage for orders (will reset if the server restarts)
orders = []

# Function to save orders to a JSON file
def save_orders():
    with open('orders.json', 'w') as f:
        json.dump(orders, f, indent=4)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get order details from the form
        order_items = request.form.getlist('order')
        total_price = request.form.get('total_price')
        customer_name = request.form.get('customer_name')
        location = request.form.get('location')
        
        # Create a new order with a timestamp
        new_order = {
            'customer_name': customer_name,
            'location': location,
            'order': order_items,
            'total_price': total_price,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        orders.append(new_order)
        save_orders()  # Save the order to the JSON file

        # Render the confirmation page
        return render_template('confirmation.html',
                               customer_name=customer_name,
                               location=location,
                               order=order_items,
                               total_price=total_price)
    return render_template('index.html')

# Admin dashboard to view all orders
@app.route('/admin')
def admin():
    return render_template('admin.html', orders=orders)

if __name__ == '__main__':
    app.run(debug=True)
