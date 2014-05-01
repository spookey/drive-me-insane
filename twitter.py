# -.- coding: utf-8 -.-

from requests_oauthlib import OAuth1Session
from textwrap import wrap
import urllib
from util import logger, getconf

request_token_url = 'https://api.twitter.com/oauth/request_token'
authorization_url = 'https://api.twitter.com/oauth/authorize'
access_token_url = 'https://api.twitter.com/oauth/access_token'

status_url = 'https://api.twitter.com/1.1/statuses/update.json'

def dialup(resource_owner_key=None, resource_owner_secret=None):
    client_key = getconf('twitter_api_key')
    client_secret = getconf('twitter_api_secret')
    return OAuth1Session(client_key,
        client_secret=client_secret,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret
        )

def send_tweet(messagetext, **args):

    mention = args.get('mention', None)
    if mention:
        users = ''.join(['@%s ' %(user) for user in mention])
        messagetext = users + messagetext
    message = wrap(messagetext, 140)

    session = dialup(resource_owner_key=getconf('twitter_oauth_token'), resource_owner_secret=getconf('twitter_oauth_token_secret'))

    if session is not None:
        try:
            for text in message:
                payload = {'status': text}
                response = session.post(status_url, payload)
                if 'errors' in response.json():
                    raise Exception('twitter error: %s' %(response.json()['errors'][-1]['message']))
        except Exception as ex:
            logger.error('error: %s' %(ex))
            return ex
        else:
            logger.info('tweet sent')
            return True

    logger.info('end twitter')

if __name__ == '__main__':
    session = dialup()
    session.fetch_request_token(request_token_url)

    request_url = session.authorization_url(authorization_url)
    print('open this link and authorize:\n%s' %(request_url))
    request_pin = input('PIN: ').strip()

    request_url = '%s&oauth_verifier=%s' %(request_url, request_pin)

    session.parse_authorization_response(request_url)

    result = session.fetch_access_token(access_token_url)

    print('"twitter_api_key": "%s",' %(getconf('twitter_api_key')))
    print('"twitter_api_secret": "%s",' %(getconf('twitter_api_secret')))
    print('"twitter_oauth_token": "%s",' %(result['oauth_token']))
    print('"twitter_oauth_token_secret": "%s",' %(result['oauth_token_secret']))
