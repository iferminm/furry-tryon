#coding=utf-8
from __future__ import unicode_literals
from backends.paypal.classes import PayPalConnection

con = PayPalConnection(username='dev_1361828047_biz_api1.lechuzacomunicaciones.com', passwd='1361828070', signature='A-SZndTAduBaeH3.JfilwnOARbRqAXlNWogNZFqZeenghqMdljswNRZp', test=True)

payment = {'amount': 18.99, 'currency_code': 'USD'}
token_data = con.request_token(return_url='http://www.google.com', cancel_url="http://yahoo.com", payment_data=payment)
print token_data
print con.get_consent_url(token=token_data['token'])
