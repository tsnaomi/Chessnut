from .models import (
    DBSession,
    TwUser,
    Game,
    Challenge,
    )
import sqlalchemy as sa
import transaction
from .generate_board import board
from .chess import ChessnutGame as cg
from gevent.queue import Queue as gqueue
import tweepy
import os
import re


consumer_key = 'a1QFgBvoQNnSbshCghSwg'
consumer_secret = '9niiLlNcfJYR4W4u5kNwQjEZEXE81HBwkHA6hRw4QU'


def tweet_parser(tweet):
    """Takes in a unicode-formatted tweet and returns a dictionary of the
    game name opponent, move, and extra message.
    """
    tweet = tweet.encode()

    match = re.match(
        r'^@\w{11} (@(?P<opponent>[^\s]+) )?#(?P<game>[\w\d]+)( (?P<move>[^\s]+))?( (?P<message>.*))?$',
        tweet
    )

    if match:
        group = match.groupdict()
        for k, v in group.iteritems():
            if v:
                group[k] = v.decode('utf-8')
        return group
    else:
        raise ValueError("Tweet not formatted correctly.")


def get_api(user):
    user = TwUser.get_by_user_id(user)
    key, secret = user.key, user.secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(key, secret)
    api = tweepy.API(auth)
    return api


def get_moves(since_id):
    api = get_api(2422730102)
    mentions = api.mentions_timeline()
    movequeue = gqueue()
    for i in mentions[-1::-1]:
        movequeue.put(i)
        since_id.value = long(i.id) + long(1)
    return since_id, movequeue


def execute_moves(movequeue):
    size = movequeue.qsize()
    for i in xrange(size):
        move = movequeue.get()
        text, user_id, user = move.text, move.user.id, move.user.screen_name
        parsed = tweet_parser(text)
        #assume it's a move and give it a shot
        try:
            game = Game.get_by_name(parsed['game'])
            if game.is_turn(user_id):
                game_update = cg(game.pgn)
                game_update(parsed['move'])
                game.pgn = game_update.pgn
                image_url = board(cg.image_string)
                send_user_tweet(user_id, image_url, game)
                game.end_turn()
            else:
                send_error(user_id, 'notyourturn')
        except:
            #this means it should be a challenge
            if parsed['opponent'] and parsed['game']:
                challenge = Challenge.get_by_name(parsed['game'])
                opponent = TwUser.get_by_user_id(user_id)
                if challenge is not None and opponent is not None:
                    if challenge.owner_sn == parsed['opponent'] and challenge.opponent == user:
                        challenge.accept(opponent.id)
                        send_game_start(parsed['game'], parsed['opponent'], user)
                    else:
                        send_error(user_id, error='notyourgame')
                elif challenge is not None:
                    send_error(user_id, error='register')
                else:
                    #making sure user_id is registered with us
                    owner = TwUser.get_by_user_id(user_id)
                    try:
                        challenge = Challenge(parsed['game'],
                                              owner.id,
                                              parsed['opponent'],
                                              user,
                                              )
                        DBSession.add(challenge)
                        send_challenge(user_id, parsed['opponent'])
                    #this is for the unregistered
                    except TypeError:
                        send_error(user_id, error='register')
                    #should be preventing duplicate game names here
                    except:
                        send_error(user_id, error='gamename')
            #formatting problems get grabbed here
            else:
                send_error(user_id, error='format')
        #and this is just us handling a normal move
    return None


def send_user_tweet(user, gamename, image_url):
    api = get_api(user)
    opponent = u'lordsheepy'
    tweet = u"@%s Gamename: %s Boardstate: %s" % (opponent, gamename, image_url)
    api.update_status(tweet)
    return


def send_challenge(user, opponent):
    """sends a challenge tweet to an opponent and an invitation to register if
    they are not an existing user"""
    api = get_api(user)
    cn_api = get_api(2422730102)
    opponent = api.get_user(opponent)
    user = api.get_user(user)
    challengetweet = u"@%s I'm challengeing you to a game of chess" % opponent.screen_name
    if not TwUser.get_by_user_id(opponent.id):
        newuser_tweet = u"@%s @%s has challenged you to a game of chess! Join by visiting %s" % (opponent.screen_name, user.screen_name, 'url goes here')
        cn_api.update_status(newuser_tweet)
    api.update_status(challengetweet)
    return


def send_game_start(name, owner, opponent):
    """sends start game tweet to owner and opponent"""
    api = get_api(2422730102)
    tweet = u"The game begins at #%s. @%s has the first move. @%s is the opponent" % (name, owner, opponent)
    api.update_status(tweet)
    return


def send_error(user, error='default'):
    error_dict = {
        'default': u"@%s There was a general error",
        'register': u"@%s you have to register to challenge people",
        'gamename': u"@%s that game name is already taken",
        'format': u"@%s Your last tweet had formatting issues",
        'notyourgame': u"@%s that is not your game",
        'notyourturn': u"@%s it isn't your turn yet",
    }
    api = get_api(2422730102)  # the user_id of @chessnutapp
    user = api.get_user(user)
    user = user.screen_name
    tweet = error_dict[error]
    tweet = tweet % user
    # api.update_status(tweet)
    return None


def media_tweet():
    api = get_api(2422730102)  # the user_id of @chessnutapp
    tweet = u"Uploading a file online @lordsheepy"
    fn = "https://www.google.com/images/srpr/logo11w.png"
    api.update_with_media(fn, status=tweet)
    return None
