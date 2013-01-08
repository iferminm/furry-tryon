#coding=utf-8

## #############################################################
## Unnamed Social Lib
## Testing module
## Coded by: Israel Fermín Montilla <ferminster@gmail.com>
## Caracas - Venezuela (2013)
## #############################################################

gmail_urls = {
    'get_access_token': 'https://accounts.google.com/o/oauth2/token',
    'get_request_token': 'https://accounts.google.com/o/oauth2/auth?%s',
    'refresh_token': 'https://accounts.google.com/o/oauth2/token',
    'get_user_contacts': 'https://www.google.com/m8/feeds/contacts/default/full?access_token=%s&max-results=30000&alt=json',
    'get_user_profile': 'https://www.googleapis.com/plus/v1/people/me?access_token=%s',
    'get_user_info': 'https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token=%s'
}

facebook_urls = {
    'get_request_token': 'https://www.facebook.com/dialog/oauth?client_id=%s&redirect_uri=%s&scope=%s',
    'get_access_token': 'https://graph.facebook.com/oauth/access_token?client_id=%s&redirect_uri=%s&client_secret=%s&code=%s',
    'get_user_friends': 'https://graph.facebook.com/me/friends?access_token=%s',
    'do_wall_post': 'https://graph.facebook.com/me/feed?message=%s&access_token=%s&link=%s',
    'get_user_info': 'https://graph.facebook.com/me?%s'
}
