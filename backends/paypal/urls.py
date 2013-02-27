#coding=utf-8
from __future__ import unicode_literals

testing_urls = {
    'endpoint': 'https://api-3t.sandbox.paypal.com/nvp',
    'authorization': 'https://www.sandbox.paypal.com/webscr?cmd=_express-checkout&token=%(token)s'
}
paypal_urls = {
    'endpoint': 'https://api-3t.paypal.com/nvp',
    'authorization': 'https://www.paypal.com/webscr?cmd=_%(command)s&token=%(token)s'
}
