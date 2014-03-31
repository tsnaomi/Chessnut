import tweepy

consumer_token = 'secret'
consumer_secret = 'totes'

auth = tweepy.OAuthHandler(consumer_token, consumer_secret)

try:
    redirect_url = auth.get_authorization_url()
except tweepy.TweepError:
    print 'Error! Failed to get request token.'

session.set('request_token', (auth.request_token.key,
            auth.request_token.secret))

# Example using callback (web app)
verifier = request.GET.get('oauth_verifier')

# Let's say this is a web app, so we need to re-build the auth handler
# first...
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
token = session.get('request_token')
session.delete('request_token')
auth.set_request_token(token[0], token[1])

try:
    auth.get_access_token(verifier)
except tweepy.TweepError:
    print 'Error! Failed to get access token.'

# store this
auth.access_token.key
auth.access_token.secret

# to re-build
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)

#to access twitter
api = tweepy.API(auth)
api.update_status('tweepy + oauth!')