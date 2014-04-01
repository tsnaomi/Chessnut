# from pyramid.response import Response
from pyramid.view import view_config
from .models import (
    DBSession,
    TwUser,
    )
import tweepy
from pyramid.httpexceptions import HTTPFound


@view_config(route_name='index', renderer='base.jinja2')
def test_view(request):
    return {}


consumer_key = 'key'
consumer_secret = 'secret'


@view_config(route_name='login', renderer='string')
def get_auth(request):
    """talks to twitter api and retrieves request token and token secret"""
    if request.session.get('user_id', 0):
        return HTTPFound(location=request.route_url('index'))
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        raise

    session = request.session
    session['request_token'] = (auth.request_token.key,
                                auth.request_token.secret)
    session.save()

    return HTTPFound(location=redirect_url)


@view_config(route_name='twauth', renderer='string')
def tw_auth(request):
    session = request.session
    verifier = request.GET.get('oauth_verifier')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    token = session.get('request_token')
    del request.session['request_token']
    auth.set_request_token(token[0], token[1])

    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        raise

    key = auth.access_token.key
    secret = auth.access_token.secret

    user = TwUser.get_by_secret(secret)

    if not user:
        user = TwUser(key, secret)
        DBSession.add(user)

    user = TwUser.get_by_secret(secret)

    session['logged_in'] = True
    session['user_id'] = user.id

    return HTTPFound(location=request.route_url('index'))


@view_config(route_name='logout', renderer='string')
def logout(request):
    del request.session['user_id']
    request.session['logged_in'] = False
    return "Logged out, bra"


@view_config(route_name='post', renderer='string')
def test_post(request):
    if request.session.get('user_id', 0):
        user = TwUser.get_by_id(request.session['user_id'])
        key, secret = user.key, user.secret
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(key, secret)
        api = tweepy.API(auth)
        api.update_status("test session management")
        return "Success"
    return "Not Logged in"
