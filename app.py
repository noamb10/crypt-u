from flask import Flask, request, render_template
from coinbase.wallet.client import Client

API_KEY = 'Ba6DEkGrqrB4M8uY'
API_SECRET = 'ICVK2n2Kl5WBQCFMzZONp2NzGG5hdcBg'
COMMISSION_RATE = 0.01 # 1% commission

client = Client(API_KEY, API_SECRET)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('template.html')

@app.route('/portfolio')
def portfolio():
    # Get the user's primary account ID
    account_id = client.get_primary_account()['id']
    # Get the user's current Bitcoin balance
    btc_balance = client.get_account(account_id)['balance']['amount']
    # Get the user's transaction history for Bitcoin purchases
    btc_transactions = client.get_transactions(account_id, limit=10, order='desc')
    # Render the portfolio template with the portfolio information
    return render_template('portfolio.html', btc_balance=btc_balance, btc_transactions=btc_transactions)

@app.route('/wallet', methods=['GET'])
def wallet():
    private_key, public_key, bitcoin_address = generate_wallet()
    return render_template('wallet.html', private_key=private_key, public_key=public_key, bitcoin_address=bitcoin_address)


@app.route('/buy', methods=['POST'])
def buy():
    amount = request.form['amount']
    address = request.form['address']
    frequency = request.form['frequency']
    # Get the current price of Bitcoin
    price = client.get_spot_price(currency_pair='BTC-USD')['amount']
    # Calculate the amount of USD needed to buy the specified amount of Bitcoin
    usd_amount = float(amount) * float(price)
    # Calculate the commission amount
    commission = usd_amount * COMMISSION_RATE
    # Calculate the net amount to invest
    net_amount = usd_amount - commission
    # Buy Bitcoin using Coinbase Commerce
    account_id = client.get_primary_account()['id']
    payment = client.buy(account_id, amount=net_amount, currency='USD', payment_method='your_payment_method_here', commit=True, cryptocurrency='BTC', destination=address)
    # Transfer the commission to your BTC wallet
    transfer = client.send_money(to=address, amount=commission, currency='USD', description='Commission')
    # Schedule recurring buys based on the user's selected frequency
    if frequency == 'week':
        client.create_recurring_buy(amount=amount, currency='BTC', payment_method='your_payment_method_here', commit=True, period='week', day_of_week='mon')
    elif frequency == 'day':
        client.create_recurring_buy(amount=amount, currency='BTC', payment_method='your_payment_method_here', commit=True, period='day')
    elif frequency == 'month':
        client.create_recurring_buy(amount=amount, currency='BTC', payment_method='your_payment_method_here', commit=True, period='month')
    elif frequency == 'custom':
        # You'll need to provide additional logic to allow the user to specify their desired custom frequency
        pass
    return {'message': f'Bought {amount} BTC for {net_amount} USD (including {commission} USD commission). Commission has been transferred to your BTC wallet. Recurring buys have been scheduled for {frequency}ly.'}

if __name__ == '__main__':
    app.run(debug=True)
