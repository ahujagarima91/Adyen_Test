
from flask import Flask, render_template, request, abort

from .main.config import read_config
from .main.payments import initiate_user_payment
from .main.payment_methods import adyen_payment_methods
import app.main.config as config

supported_integrations = ['dropin','ideal']

def create_app():
    app = Flask('app')

    app.register_error_handler(404, page_not_found)

    # read confis from config file
    read_config()

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/cart/<integration>')
    def cart(integration):
        return render_template('cart.html', method=integration)

    @app.route('/checkout/<integration>')
    def checkout(integration):
        client_key = config.client_key
        try:
            if integration in supported_integrations:
                return render_template('component.html', method=integration, client_key=client_key)
        except:
            abort(404)

    @app.route('/api/getPaymentMethods', methods=['GET', 'POST'])
    def get_payment_methods():
        return adyen_payment_methods()

    @app.route('/api/initiatePayment', methods=['POST'])
    def initiate_payment():
        return initiate_user_payment(request)

    @app.route('/result/success', methods=['GET'])
    def checkout_success():
        return render_template('checkout-success.html')

    @app.route('/result/failed', methods=['GET'])
    def checkout_failure():
        return render_template('checkout-failed.html')

    @app.route('/result/pending', methods=['GET'])
    def checkout_pending():
        return render_template('checkout-success.html')

    @app.route('/result/error', methods=['GET'])
    def checkout_error():
        return render_template('checkout-failed.html')

  #  return app
    app.run()


def page_not_found(error):
    return render_template('error.html'), 404
