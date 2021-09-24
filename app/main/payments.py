import app.main.config as config
import Adyen
import uuid
import json

def initiate_user_payment(frontend_request):
	adyen = Adyen.Adyen()
	adyen.client.platform = 'test'
	adyen.client.xapikey = config.checkout_apikey

	payment_info = frontend_request.get_json()
	order_ref = str(uuid.uuid4())

	payments_request = {
		'amount': {
			'value': 1000,
			'currency': "USD"
		},
		'channel': 'Web',
		'reference': order_ref,
		'shopperReference': "Python Checkout Shopper",
		'returnUrl': "http://localhost:8080/api/handleShopperRedirect?orderRef=" + order_ref,
		'countryCode': 'NL',
		'shopperLocale': "en_NL",
		'storePaymentMethod': 'true',
		'merchantAccount': config.merchant_account
	}
	payments_request.update(payment_info)

	print("/payments request:\n" + str(payments_request))

	payments_response = adyen.checkout.payments(payments_request)
	formatted_response = json.dumps((json.loads(payments_response.raw_response)))

	print("/payments response:\n" + formatted_response)
	return formatted_response
