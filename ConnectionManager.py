#coding=utf-8
from __future__ import unicode_literals
from backends.facebook import FacebookConnection
from backends.twitter import TwitterConnection
from backends.gmail import GmailConnection

__connections = {
    'gmail': GmailConnection(),
    'facebook': FacebookConnection(),
    'twitter': TwitterConnection
}

def connect_with(which):
    return __connection[which]
