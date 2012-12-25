#coding=utf-8
from __future__ import unicode_literals
import simplejson
import urllib
import urllib2
import urlparse
import settings

class FacebookConnection:
    '''
    Manages the interaction with facebook accounts
    '''
    def __init__(self):
        self.key = settings.FACEBOOK_KEY
        self.secret = settings.FACEBOOK_SECRET
        self.scope = ','.join(settings.FACEBOOK_SCOPE)
        self.callback = settings.FACEBOOK_CALLBACK

    def request_consent(self):
        '''
        Generates an URL to request user consent to access his account
        '''
        from social_urls import facebook_urls
        result = {
            'redirect_url': facebook_urls['get_request_token'] % (self.key, self.callback, self.scope),
        }
        return result

    def request_access(self, code):
        '''
        Requests the access token to the user's account
        '''
        from social_urls import facebook_urls
        access_uri = facebook_urls['get_access_token'] % (self.key, self.callback, self.secret, code)
        result = urllib2.urlopen(access_uri).read()
        result_data = dict(urlparse.parse_qsl(result))
        return result_data

    def get_all_user_friends(self, access_token):
        '''
        Gets all user's friends and returns them in json format without
        paging
        '''
        from social_urls import facebook_urls
        result = urllib2.urlopen(facebook_urls['get_user_friends'] % access_token)
        data = simplejson.loads(result.read())
        friends = []
        while len(data['data']) > 0:
            friends.extend(data['data'])
            if data['paging'].has_key('next'):
                result = urllib2.urlopen(data['paging']['next'])
                data = simplejson.loads(result.read())
            else:
                break
        return friends

    def wall_post(self, access_token, text, link):
        '''
        Publishes a wallpost with a link attatched
        '''
        from social_urls import facebook_urls
        data = {
                'message': text,
                'link': link,
                'access_token': access_token,
            }
        result = urllib2.urlopen(facebook_urls['do_wall_post'], data=urllib.urlencode(data))
        data = simplejson.loads(result.read())
        return data

    def get_user_fields(self, access_token, fields):
        '''
        Gets information about the logged user
        '''
        from social_urls import facebook_urls
        params = {
                'fields': ','.join(fields),
                'access_token': access_token,
            }
        url = facebook_urls['get_user_info'] % urllib.urlencode(params)
        result = urllib2.urlopen(url)
        return simplejson.loads(result.read())
