from flask import Flask, render_template, request

app = Flask(__name__)

# Simulated database for menu items
menu_items = [
    {"id": 1, "name": "Coffee", "price": 2.0, "description": "Hot coffee"},
    {"id": 2, "name": "Tea", "price": 1.5, "description": "Herbal tea"},
    {"id": 3, "name": "Sandwich", "price": 3.5, "description": "Ham & cheese sandwich"}
]

# Simulated orders storage
orders = []

@app.route('/')
def index():
    return render_template('index.html', menu_items=menu_items)

@app.route('/order', methods=['POST'])
def order():
    # Get selected items from the form
    selected_ids = request.form.getlist('item')
    order_total = 0
    order_details = []

    for item_id in selected_ids:
        for item in menu_items:
            if str(item['id']) == item_id:
                order_details.append(item)
                order_total += item['price']
                break

    # Create and store order (in a real system, this would be stored in a database)
    order_id = len(orders) + 1
    order_data = {"id": order_id, "details": order_details, "total": order_total}
    orders.append(order_data)
    
    return render_template('confirmation.html', order=order_data)

if __name__ == '__main__':
    app.run(debug=True)
