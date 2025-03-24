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
    'cheeseburger': {'name': 'Cheeseburger', 'price': 15000},
    'cheese Sandwich': {'name': 'Cheese Sandwich', 'price': 18000},
    'chicken burgers': {'name': 'Chicken Burgers', 'price': 25000},
    'spicy chicken': {'name': 'Spicy Chicken', 'price': 22000},
    'hot dog': {'name': 'Hot Dog', 'price': 10000},
    'fruit salad': {'name': 'Fruit Salad', 'price': 8000},
    'Cocktails': {'name': 'Cocktails', 'price': 18000},
    'Nuggets': {'name': 'Nuggets', 'price': 9000},
    'Sandwich': {'name': 'Sandwich', 'price': 16000},
    'French Fries': {'name': 'French Fries', 'price': 7000},
    'Milk Shake': {'name': 'Milk Shake', 'price': 3000},
    'Iced Tea': {'name': 'Iced Tea', 'price': 2000},
    'Orange Juice': {'name': 'Orange Juice', 'price': 2500},
    'Lemon Tea': {'name': 'Lemon Tea', 'price': 1500}
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
