from flask import Flask, render_template, request

app = Flask(__name__)

# Route to display the menu
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the order data from the form
        order = request.form.getlist('order')
        total_price = request.form.get('total_price')
        
        # Display the order on the confirmation page
        return render_template('confirmation.html', order=order, total_price=total_price)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
