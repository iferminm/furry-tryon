# coding=utf-8
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.conf import settings
from django.utils.translation import ugettext as _
import oauth2 as oauth
import urllib2
import urllib
import urlparse
import tweepy
import logging
import social_urls

logger = logging.getLogger(__name__)

class TwitterConnection:
    '''
    Manages all the interaction with twitter accounts
    '''
    def __init__(self):
        self.key = settings.TWITTER_KEY
        self.secret = settings.TWITTER_SECRET
        self.callback = settings.TWITTER_CALLBACK

    def request_consent(self):
        '''
        Generates an URL to request user consent to access his account
        '''
        auth = tweepy.OAuthHandler(self.key, self.secret, self.callback)
        try:
            redirect_url = auth.get_authorization_url()
            result = {
                    'redirect_url': redirect_url,
                    'request_token': auth.request_token.key,
                    'request_token_secret': auth.request_token.secret,
                }
            return result
        except:
            logger.exception('Se produjo un error no controlado')
        return {'ERROR': _('We couldn\'t connect with twitter server, please try again in a few minutes')} 

    def request_access(self, oauth_verifier, request_token, request_secret):
        '''
        Requests access credentials (token and secret) to make
        use of our permissions
        '''
        auth = tweepy.OAuthHandler(self.key, self.secret)
        auth.set_request_token(request_token, request_secret)
        auth.get_access_token(oauth_verifier)
        result = {
                'access_token': auth.access_token.key,
                'access_token_secret': auth.access_token.secret
            }
        return result

    def tweet(self, message, access_token, token_secret):
        '''
        Publishes a given message on the active user's twitter
        account
        '''
        auth = tweepy.OAuthHandler(self.key, self.secret)
        auth.set_access_token(access_token, token_secret)
        twitter = tweepy.API(auth)
        result = twitter.update_status(message)
        return {'response': result,}


class GmailConnection:
    '''
    Manages all the interaction with Gmail accounts
    '''
    def __init__(self):
        self.key = settings.GMAIL_KEY
        self.client_id = settings.GMAIL_CLIENT
        self.secret = settings.GMAIL_SECRET
        self.scope = settings.GMAIL_SCOPE
        self.callback = settings.GMAIL_CALLBACK

    def request_consent(self):
        '''
        Generates an URL to request user consent to access his account
        '''
        from social_urls import gmail_urls
        parameters = {
                'response_type': 'code',
                'client_id': self.client_id,
                'redirect_uri': self.callback,
                'scope': self.scope,
                'states': 'contacts',
                'access_type': 'offline',
                'approval_prompt': 'force',
            }
        
        result = {
                'redirect_url': gmail_urls['get_request_token'] % urllib.urlencode(parameters),
            }
        return result

    def request_access(self, auth_code):
        '''
        Requests access and refresh tokens
        '''
        from social_urls import gmail_urls
        post_data = {
                'code': auth_code,
                'client_id': self.client_id,
                'client_secret': self.secret,
                'redirect_uri': self.callback,
                'grant_type': 'authorization_code',
            }
        response = urllib2.urlopen(gmail_urls['get_access_token'], urllib.urlencode(post_data))
        result = simplejson.loads((response.read().replace('\n', '')))
        return result

    def refresh_token(self, refresh_token):
        '''
        Refreshes an expired token and provides a new
        access token
        '''
        from social_urls import gmail_urls
        data = {
                'client_id': self.client_id,
                'client_secret': self.secret,
                'refresh_token': refresh_token,
                'grant_type': 'refresh_token',
            }
        result = urllib2.urlopen(gmail_urls['refresh_token'], data=urllib.urlencode(data))
        token_info = simplejson.loads(result.read())
        return token_info

    def get_user_contacts(self, access_token):
        '''
        Gets all the user contacts and returns them in json format
        '''
        from social_urls import gmail_urls
        contacts = urllib2.urlopen(gmail_urls['get_user_contacts'] % access_token)
        return simplejson.loads(contacts.read())

    def get_user_info(self, access_token):
        from social_urls import gmail_urls
        user_info = urllib2.urlopen(gmail_urls['get_user_info'] % access_token)
        return simplejson.loads(user_info.read())

    def get_my_profile(self, access_token):
        from social_urls import gmail_urls
        user_info = urllib2.urlopen(gmail_urls['get_user_profile'] % access_token)
        return simplejson.loads(user_info.read())

    # TODO: este método no funciona, hay que investigar un poco cómo trabaja 
    # Google Contacts API v3 con las imágenes, quizás hacer conexión con G+ 
    # en lugar de Gmail como tal
    def get_contact_photo(self, access_token):
        '''
        Should look for the contacts photo, currently not workink
        '''
        test_url = 'http://www.google.com/m8/feeds/contacts/ferminster%40gmail.com/base/2' + '?access_token=%s' % access_token
        info = urllib2.urlopen(test_url)

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

class LinkedinConnection:
    '''
    Manages connection and interaction with Linkedin
    '''
    def __init__(self):
        self.token = settings.LINKEDIN_KEY
        self.secret = settings.LINKEDIN_SECRET
        self.callback = settings.LINKEDIN_CALLBACK

    def request_consent(self, request):
        '''
        Shows the consent form to the user so we can access
        his linkedin data and connections
        '''
        consumer = oauth.Consumer(self.token, self.secret)
        client = oauth.Client(consumer)
        response, content = client.request(social_urls.LINKEDIN_REQUEST_TOKEN_URL % self.callback)
        token_data = dict(urlparse.parse_qsl(content))
        request.session['oauth_data'] = token_data
        auth_url = social_urls.LINKEDIN_AUTH_URL % (token_data['oauth_token'], self.callback)
        result = {
                'redirect_url': auth_url,
            }
        return result

    def request_access(self, oauth_verifier, oauth_token, oauth_token_secret):
        '''
        Gets a LinkedIn access token
        '''
        consumer = oauth.Consumer(self.token, self.secret)
        token = oauth.Token(oauth_token, oauth_token_secret)
        token.set_verifier(oauth_verifier)

        client = oauth.Client(consumer, token)
        response, content = client.request(social_urls.LINKEDIN_ACCESS_URI)
        token_data = dict(urlparse.parse_qsl(content))
        return token_data

    def get_user_connections(self):
        return {'error': _('not implemented yet')}

class OrkutConnection:
    '''
    Manages connection with Orkut
    '''
    def __init__(self):
        self.client_id = settings.ORKUT_CLIENT
        self.key = settings.ORKUT_KEY
        self.secret = settings.ORKUT_SECRET
        self.scopes = settings.ORKUT_SCOPE
        self.callback = settings.ORKUT_CALLBACK

    def request_consent(self):
        '''
        Generates an URL to request user consent to access his account
        '''
        parameters = {
                'response_type': 'code',
                'client_id': self.client_id,
                'redirect_uri': self.callback,
                'scope': ','.join(self.scopes),
                'states': 'contacts',
                'access_type': 'offline',
                'approval_prompt': 'force',
            }

        result = {
                'redirect_url': social_urls.GMAIL_REQUEST_TOKEN_URI % urllib.urlencode(parameters),
            }
        return result

    def request_access(self, auth_code):
        '''
        Requests access and refresh tokens
        '''
        post_data = {
                'code': auth_code,
                'client_id': self.client_id,
                'client_secret': self.secret,
                'redirect_uri': self.callback,
                'grant_type': 'authorization_code',
            }
        response = urllib2.urlopen(social_urls.GMAIL_ACCESS_TOKEN_URI, urllib.urlencode(post_data))
        result = simplejson.loads((response.read().replace('\n', '')))
        return result

    def get_user_contacts(self):
        return {'error': _('Not implemented yet')}

__connections = {
    'gmail': GmailConnection(),
    'twitter': TwitterConnection(),
    'facebook': FacebookConnection(),
    'linkedin': LinkedinConnection(),
    'orkut': OrkutConnection(),
}

def connect_with(which):
    return __connections[which]
