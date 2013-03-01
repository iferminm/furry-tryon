#coding=utf-8
from __future__ import unicode_literals
from urls import testing_urls, checkout_urls
import simplejson
import urllib
import urllib2


class GoogleCheckoutConnection(object):
    """
    This class manages the interaction with
    google checkout service
    """
    def __init__(self, merchant_id, test=False):
        self.urls = testing_urls if testing else checkout urls

