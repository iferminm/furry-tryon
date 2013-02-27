#coding=utf-8
from __future__ import unicode_literals
from urls import testing_urls, paypal_urls
from currencies import * 
import urllib
import urllib2
import simplejson

class PayPalConnection(object):
    """
    This class manages the interaction with paypal API
    """
    def __init__(self, username, passwd, signature, test=False):
        """
        username: api username for the application
        passwd: api password for the application
        signature: api signature for the application

        All this values parameters are available from your paypal
        business account under the API Access section.
        """
        self.urls = testing_urls if test else paypal_urls
        self.api_username = username
        self.api_passwd = passwd
        self.api_signature = signature

    def request_token(self, return_url, cancel_url, payment_data):
        """
        This function requests an access token to PayPal API
        so we can proceed with the payment process.

        return_url: success callback URL
        cancel_url: fail callback url
        payment_data: dictionary {'amount': value, 'currency_code': 'CODE' or None}
        return dict: all the response parameters in a python dictionari
        """
        post_data = {
            'USER': self.api_username,
            'PWD': self.api_passwd,
            'SIGNATURE': self.api_signature,
            'VERSION': '84.0',
            'PAYMENTREQUEST_0_PAYMENTACTION': 'Sale',
            'PAYMENTREQUEST_0_AMT': payment_data['amount'],
            'PAYMENTREQUEST_0_CURRENCYCODE': payment_data.get('currency_code', False) or 'USD',
            'RETURNURL': return_url,
            'CANCELURL': cancel_url,
            'METHOD': 'SetExpressCheckout'
        }

        response = urllib2.urlopen(urls['endpoint'], urllib.urlencode(post_data))
        content = [tuple(v.split('=')) for v in urllib.unquote(response.read()).split('&')]
        content = {k.lower(): v for k, v in content}

        return content

    def get_consent_url(self, token):
        """
        returns a token-signed url to ask permission
        to use his paypal account
        """
        return self.urls % {'command': 'express-checkout', 'token': token}

