# from pyramid.response import Response
from pyramid.view import view_config
from pyramid import request
from .models import (
    DBSession,
    TwUser,
    SinceId,
    Game,
    )
import transaction
import tweepy
from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    HTTPError,
    exception_response
    )
from paste.deploy.loadwsgi import appconfig

config = appconfig('config:development.ini', 'main', relative_to='.')

consumer_key = config['consumer_key']
consumer_secret = config['consumer_secret']


@view_config(route_name='moves', renderer='string')
def moves_view(request):
    moves()
    return "Crap was done."


@view_config(route_name='home', renderer='home.jinja2')
def home_view(request):
    if request.session.get('logged_in', 0):
        open_games, games = {}, Game.get_by_person(request.session.get('user_id', 0))
        for game in games:
            if not game.is_over:
                open_games[game] = game.get_boards()
        return {'session': request.session, 'open': open_games}
    return {'session': request.session}


@view_config(route_name='list', renderer='list.jinja2')
def list_view(request):
    id = int(request.matchdict.get('id', -1))
    try:
        # import pdb; pdb.set_trace()
        user = TwUser.get_by_id(id)
        closed_games, open_games, games = {}, {}, Game.get_by_person(id)
        for game in games:
            if game.is_over:
                closed_games[game] = game.get_boards()
            else:
                open_games[game] = game.get_boards()
        return {'id': id, 'user': user, 'session': request.session,
                'closed': closed_games, 'open': open_games}
    except HTTPError:
        raise exception_response(404)


@view_config(route_name='match', renderer='details.jinja2')
def details_view(request):
    game = Game.get_by_name(request.matchdict.get('name', -1))
    if game:
        return {'session': request.session, 'game': game}
    return HTTPNotFound


@view_config(route_name='notation', renderer='notation.jinja2')
def notation_view(request):
    return {'session': {}}


@view_config(route_name='login', renderer='string')
def get_auth(request):
    """talks to twitter api and retrieves request token and token secret"""
    if request.session.get('user_id', 0):
        # return HTTPFound(location=request.route_url('index'))
        return HTTPFound(location=request.route_url('home'))
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
    # return HTTPFound(location=request.route_url('home'))


@view_config(route_name='twauth', renderer='string')
def tw_auth(request):
    session = request.session
    verifier = request.GET.get('oauth_verifier')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth)
    token = session.get('request_token')
    del request.session['request_token']
    auth.set_request_token(token[0], token[1])

    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        raise

    key = auth.access_token.key
    secret = auth.access_token.secret
    twuser = api.me()

    user = TwUser.get_by_secret(secret)

    if not user:
        user = TwUser(key, secret, twuser.id, twuser.screen_name)
        DBSession.add(user)

    user = TwUser.get_by_secret(secret)

    session['logged_in'] = True
    session['user_id'] = user.id
    session['username'] = twuser.screen_name

    return HTTPFound(location=request.route_url('home'))


@view_config(route_name='logout', renderer='string')
def logout(request):
    del request.session['user_id']
    request.session['logged_in'] = False
    return "Logged out, bra"
