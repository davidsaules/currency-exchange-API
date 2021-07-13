from threading import Lock
from flask import jsonify, make_response, abort

class CurrencyExchange():

	feesCharged = 0;

	def __init__(self):
		# it is used to assure atomic currency exchange
		self.lock = Lock()
		# we choose USD as a base to convert currencies
		self.base = "USD"
		# save
		self.rates = {
			"USD": {"rate": 1.0, "amount": 1000, "fee": 1.0},
			"AUD": {"rate": 1.335, "amount": 1000, "fee": 1.3},
			"CAD": {"rate": 1.244, "amount": 1000, "fee": 1.7},
			"CHF": {"rate": 0.914, "amount": 1000, "fee": 1.1},
			"EUR": {"rate": 0.842, "amount": 1000, "fee": 1.5},
			"GBP": {"rate": 0.719, "amount": 1000, "fee": 1.9},
			"JPY": {"rate": 110.200, "amount": 1000, "fee": 1.8},
			"NZD": {"rate": 1.427, "amount": 1000, "fee": 1.4}
		}

	def getExchangeRate(self, base_currency, quote_currency):

		# assure currencies chosen are available
		if not (base_currency in self.rates and quote_currency in self.rates):
			abort(make_response(jsonify({
				"result": "failure",
				"message": "Exchange between those currencies is not available",
				"error": 400
				}), 400))

		fee = 0.0
		rate = 0.0

		# convert it into our base currency if we need it
		if base_currency != self.base:
			rate = 1 / self.rates[base_currency]["rate"]
			fee = 1 / self.rates[base_currency]["fee"]

		rate = round(rate * self.rates[quote_currency]["rate"], 4)
		# round up to 2 digits because it represent percentage
		fee = round(fee * self.rates[quote_currency]["fee"], 2)

		return {
			"rate": rate, "fee": fee, 
			"available": self.rates[quote_currency]["amount"]
			}


	def exchangeCurrency(self, base_currency, quote_currency, amount):

		exchage_rate = self.getExchangeRate(base_currency, quote_currency)
		rate = exchage_rate["rate"]
		fee = exchage_rate["fee"]

		# total fee charged in the base currency. 
		# the total fee is divided by the base currency 
		# to convert it into our base (USD)
		total_fee = amount * (rate * (fee / 100))
		total_fee_base = round(total_fee / self.rates[base_currency]["rate"],4)
		# rate with fee charged
		rate = round(rate - (rate * (fee / 100)), 4)
		# then, we convert base currency into quote currency
		final_amount = round(rate * amount, 4)		

		# we make the exchange, update the charged fee and update amounts of 
		# base currency and quote currency
		if final_amount <= self.rates[quote_currency]["amount"]:
			# start the atomic operation
			self.lock.acquire()

			try:
				self.rates[base_currency]["amount"] += amount
				self.rates[quote_currency]["amount"] -= final_amount

				self.feesCharged += total_fee_base
			finally:
				# ends atomic operation
				self.lock.release()

			return {"final_amount": final_amount, "quote_currency": quote_currency}
		else:
			abort(make_response(jsonify({
				"result": "failure",
				"message": "There is no enough amount of money",
				"error": 404
			}), 404))





