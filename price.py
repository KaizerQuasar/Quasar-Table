from flask import Flask, request

app = Flask(__name__)

@app.route('/yoururl', methods=['POST'])
def receive_prices():
    global prices
    prices = request.json
