from flask import Flask, jsonify, request
from currency_exchange import CurrencyExchange

app = Flask(__name__)

currencyEx = CurrencyExchange()

# get the exchange rate between currencies
@app.route('/exchange_rate', methods=['POST'])
def getRate():

	base_c = request.json['base_currency'].upper()
	quote_c = request.json['quote_currency'].upper()
	exRate_query = currencyEx.getExchangeRate(base_c,quote_c)

	return jsonify({"query": exRate_query})

@app.route('/exchange_currency', methods=['POST'])
def exchangeCurrency():

	base_c = request.json['base_currency'].upper()
	quote_c = request.json['quote_currency'].upper()
	amount = request.json['amount']

	amount_f = currencyEx.exchangeCurrency(base_c,quote_c,amount)

	return jsonify({"result": amount_f})
