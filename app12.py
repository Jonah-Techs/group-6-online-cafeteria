from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import json

app = Flask(__name__)
app.secret_key = 'my_super_secret_key'

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

def get_price(item):
    """Returns the price of an item from the menu."""
    return menu.get(item, {}).get('price', 0)  # Default price is 0 if item is not found

# Function to save orders to a JSON file
def save_orders():
    with open("orders.json", "w") as f:
        json.dump(orders, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html', menu=menu)

@app.route('/order-approval', methods=['POST'])
def order_approval():
    customer_name = request.form.get('customer_name')
    location = request.form.get('location')
    selected_items = request.form.getlist('order')
    
    order_details = []
    total_price = 0
    for item_key in selected_items:
        item = menu.get(item_key)
        if item:
            order_details.append({'name': item['name'], 'price': item['price']})
            total_price += item['price']

    return render_template('order_approval.html',
                       customer_name=customer_name,
                       location=location,
                       order=order_details,
                       total_price=total_price)

@app.route('/submit_order', methods=['POST'])
def submit_order():
    if request.method == 'POST':
        name = request.form.get('customer_name')  # Changed from 'name' to 'customer_name'
        location = request.form.get('location')
        items = request.form.getlist('order')  # Changed from 'items' to 'order'

        order_details = []
        total_price = 0

        for item_key in items:
            item = menu.get(item_key)
            if item:
                order_details.append({'name': item['name'], 'price': item['price']})
                total_price += item['price']

        session['order'] = {
            'name': name,
            'location': location,
            'items': order_details,
            'total_price': total_price
        }

        flash("Order submitted successfully!", "success")

        return redirect(url_for('confirmation'))

    return redirect(url_for('index'))  # Fallback if something goes wrong
@app.route('/admin')
def admin():
    return render_template('admin.html', orders=orders)

@app.route('/confirmation')
def confirmation():
    order = session.get('order', {})  # Get order from session
    if not order:
        flash("No order found. Please place an order first.", "error")
        return redirect(url_for('index'))

    print(order)  # Debugging: Print the order to the console

    return render_template('confirmation.html', order=order)
if __name__ == '__main__':
    app.run(debug=True)
