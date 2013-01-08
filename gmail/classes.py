#coding=utf-8

## #############################################################
## Unnamed Social Lib
## Gmail API interaction module
## Coded by: Israel Fermín Montilla <ferminster@gmail.com>
## Caracas - Venezuela (2012)
## #############################################################
import urls
import scopes

#TODO: Fix and test this class with the new structure
class GmailWrapper:
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


