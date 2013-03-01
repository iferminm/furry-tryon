#coding=utf-8
#Everything returns a Python Dictionary
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
        return dict: all the response parameters in a python dictionary

        API Response Sample:
           TOKEN=EC%2d470284976K7901234&ACK=Success
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

        response = urllib2.urlopen(self.urls['endpoint'], urllib.urlencode(post_data))
        content = [tuple(v.split('=')) for v in urllib.unquote(response.read()).split('&')]
        content = {k.lower(): v for k, v in content}

        return content

    def get_consent_url(self, token):
        """
        returns a token-signed url to ask permission
        to use his paypal account
        """
        return self.urls['authorization'] % {'command': 'express-checkout', 'token': token}

    def get_payer_id(self, token):
        """
        Retrieves the buyer's info and returns it in a 
        Python Dict

        token: the token the API gave you in the first 
            step of the cycle

        returns: a python dictionary with the response status and the payer's id 

        API Response Sample:
            TOKEN=EC%2d470284976K7901234&ACK=Success&PAYERID=3TXTXECKFU1234
        """
        post_data = {
            'USER': self.api_username,
            'PWD': self.api_passwd,
            'SIGNATURE': self.api_signature,
            'VERSION': '84.0',
            'METHOD': 'GetExpressCheckout',
            'TOKEN': token
        }

        response = urllib2.urlopen(self.urls['endpoint'], urllib.urlencode(post_data))

        content = [tuple(v.split('=')) for v in urllib.unquote(response.read()).split('&')]
        content = {k.lower(): v for k, v in content}

        return content

    def confirm_payment(self, token, payer_id, payment_data):
        """
        Confirms the payment action in PayPal

        token: the token given in the SetExpressCheckout call
        payerid: the payerid given in the GetExpressCheckout call
        payment_data: dictionary --example--> {'amount': 20.00, 'currency_code': 'MXP'}

        returns: 
            token: the same given token
            ack: success or fail
            paymentinfo: dictionary
                transaction_id: user for authorization in payment capture
                securemetchantaccountid: unique mercharnt customer account

        API Response sample:
            TOKEN=EC%2d470284976K7901234
            &ACK=Success
            &VERSION=95
            &PAYMENTINFO_0_TRANSACTIONID=20K92515TX2901234    #Use this value as the authorization ID in a DoCapture request
            &PAYMENTINFO_0_SECUREMERCHANTACCOUNTID=QJSRDC4JW1234
            &PAYMENTINFO_0_ACK=Success
        """
        post_data = {
            'USER': self.api_username,
            'PWD': self.api_passwd,
            'SIGNATURE': self.api_signature,
            'METHOD': 'DoExpressCheckout',
            'VERSION': '84.0',
            'TOKEN': token,
            'PAYERID': payer_id,
            'PAYMENTREQUEST_0_PAYMENTACTION': 'Authorization',
            'PAYMENTREQUEST_0_AMT': payment_data['amount'],
            'PAYMENTREQUEST_0_CURRENCYCODE': payment_data.get('currency_code', False) or 'USD'
        }

        response = urllib2.urlopen(self.urls['endpoint'], urllib.urlencode(post_data))
        content = [tuple(v.split('=')) for v in urllib.unquote(response.read()).split('&')]
        content = {k.lower(): v for k, v in content}

        return content

    def capture_payment(self, auth_id, payment_data):
        """
        Captures the authorized payment.

        auth_id: the authorizarionid given in the DoExpressCheckout call
        payment_data: dictionaty with payment data --example--> {'amount': 20.00, 'currency_code': 'MXP'}

        API Response Sample:
            AUTHORIZATIONID=20K92515TX2901234
            &ACK=Success
            &TRANSACTIONID=2KF46316MJ7751234    #New transaction ID for this payment
            &PARENTTRANSACTIONID=20K92515TX2901234    #Same as the ID of the original authorization
            &TRANSACTIONTYPE=expresscheckout
            &PAYMENTTYPE=instant
            &AMT=1%2e00
            &FEEAMT=0%2e33
            &TAXAMT=0%2e00
            &CURRENCYCODE=USD
            &PAYMENTSTATUS=Completed
        """
        post_data = {
            'USER': self.api_username,
            'PWD': self.api_passwd,
            'SIGNATURE': self.api_signature,
            'METHOD': 'DoCapture',
            'VERSION': '84.0',
            'AUTHORIZATIONID': auth_id,
            'AMT': payment_data['amount'],
            'CURRENCYCODE': payment_data.get('currency_code', False) or 'USD',
            'COMPLETETYPE': 'Complete'
        }

        response = urllib2.urlopen(self.urls['endpoint'], urllib.urlencode(post_data))
        content = [tuple(v.split('=')) for v in urllib.unquote(response.read()).split('&')]
        content = {k.lower(): v for k, v in content}

        return content
