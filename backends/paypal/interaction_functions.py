#coding=utf-8
from __future__ import unicode_literals
from urls import testing_urls, paypal_urls
import urllib
import urllib2
import simplejson

def request_token(user, password, signature, return_url, cancel_url, test=False):
    """
    This function requests an access token to PayPal API
    so we can proceed with the payment process.

    user: PayPal Business account API Username
    password: Paypal API Password
    signature: Paypal API signature
    return_url: success callback URL
    cancel_url: fail callback url
    test: paypal url set to be used

    return dict: all the response parameters in a python dictionari
    """
    urls = testing_urls if test else paypal_urls
    post_data = {
        'USER': user,
        'PWD': password,
        'SIGNATURE': signature,
        'VERSION': '84.0',
        'PAYMENTREQUEST_0_PAYMENTACTION': 'Sale',
        'PAYMENTREQUEST_0_AMT': 20.00,
        'RETURNURL': return_url,
        'CANCELURL': cancel_url,
        'METHOD': 'SetExpressCheckout'
    }

    response = urllib2.urlopen(urls['endpoint'], urllib.urlencode(post_data))
    content = [tuple(v.split('=')) for v in urllib.unquote(response.read()).split('&')]
    content = {k.lower(): v for k, v in content}

    return content

def request_consent(token, test=False):
    """docstring for request_consent"""
    urls = testing_urls if test else paypal_urls

    print testing_urls['authorization'] % {'token': token}

if __name__ == '__main__':
    token = request_token('dev_1361828047_biz_api1.lechuzacomunicaciones.com', '1361828070', 'A-SZndTAduBaeH3.JfilwnOARbRqAXlNWogNZFqZeenghqMdljswNRZp', 'http://google.com', 'http://yahoo.com', test=True)
    request_consent(token['token'], test=True)

