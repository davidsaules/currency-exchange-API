# Currency exchange API
Small API that querys and exchange rate and exchange currencies.


## Instructions to run the project
It is necesary to install Docker and Docker compose  in order to deploy the project.


- To run the project, execute the following command in the `/currency_exchange` folder:
``` $ sudo docker-compose up```
(It must be where **yml** file is located)
- Once the project is running, we can consume the api on `http://localhost:5000/`
## How to consume the API

There are two available operations:

- Query an exchange rate `http://localhost:5000/exchange_rate`
- Exchange a currency `http://localhost:5000/exchange_currency`

Both operations receive and return JSON formatted values and the parameters are: **base_currency**, **quote_currency** and **amount** (if is *exchange_currency* case).

Here is an example of the exchange currency operation `http://localhost:5000/exchange_currency` with JSON format parameters:

`{ "base_currency": "AUD","quote_currency": "EUR", "amount": 200 }`



