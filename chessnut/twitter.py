from .models import (
    DBSession,
    TwUser,
    Game,
    Challenge,
    )
import sqlalchemy as sa
from .generate_board import board
from .chess import ChessnutGame as cg
import tweepy
import os
import re


consumer_key = ''
consumer_secret = ''


def tweet_parser(tweet):
    """Takes in a unicode-formatted tweet and returns a dictionary of the
    game name opponent, move, and extra message.
    """
    tweet = tweet.encode('utf-8')

    match = re.match(
        r'^@\w{11} (@(?P<opponent>[^\s]+) )?#(?P<game>\w+) (?P<move>[^\s]+) (?P<message>.*)$',
        tweet
    )

    if match:
        group = match.groupdict()
        for k, v in group:
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


def get_moves(movequeue, since_id):
    api = get_api(2422730102)
    mentions = api.mentions_timeline()
    for i in mentions[-1::-1]:
        movequeue.put(i)
        since_id.value = i.id_str
    return since_id


def execute_moves(movequeue):
    size = movequeue.qsize()
    for i in xrange(size):
        move = movequeue.get()
        text, user = move.text, move.user.id
        parsed = tweet_parser(text)
        #if there is no move, we have to figure out what it is
        if not parsed['move']:
            #this means it should be a challenge
            if parsed['opponent'] and parsed['game']:
                challenge = Challenge.get_by_name(parsed['game'])
                #determining if it is accepting or declaring a challenge
                if challenge.opponent == parsed['opponent'] and challenge.owner == user:
                    challenge.accept()
                    send_game_start(parsed['game'], user, parsed['opponent'])
                else:
                    #making sure user is registered with us
                    owner = TwUser.get_by_user_id(user)
                    try:
                        challenge = Challenge(parsed['game'],
                                              owner.id,
                                              parsed['opponent'])
                        send_challenge(user, parsed['opponent'])
                    #this is for the unregistered
                    except TypeError:
                        send_error(user, error='register')
                    #should be preventing duplicate game names here
                    except:
                        send_error(user, error='gamename')
            #formatting problems get grabbed here
            else:
                send_error(user, error='format')
        #and this is just us handling a normal move
        else:
            try:
                game = Game.get_by_name(parsed['game'])
                if game.is_turn(user):
                    game_update = cg(game.pgn)
                    game_update(parsed['move'])
                    game.pgn = game_update.pgn
                    image_url = board(cg.image_string)
                    send_user_tweet(user, image_url, game)
                    game.end_turn()
            except cg.ChessnutError as e:
                send_error(user, error=e)
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
    challengetweet = u"@%s You have been challenged to a game of chess by \
        @%s" % (opponent.screen_name, user.screen_name)
    if not TwUser.get_by_user_id(opponent.id):
        cn_api.update_status(u"@%s has challenged you to a game of chess! Join\
            by visiting %s") % (user.screen_name, 'url goes here')
    api.update_status(challengetweet)
    return


def send_game_start(name, owner, opponent):
    """sends start game tweet to owner and opponent"""
    pass


def send_error(user, error='default'):
    error_dict = {
        'default': u"There was a general error",
        'register': u"you have to reigster to challenge people",
        'gamename': u"that name is already taken",
        'format': u"Your last tweet had formatting issues",
    }
    api = get_api(2422730102)  # the user_id of @chessnutapp
    user = api.get_user(user)
    user = user.screen_name
    tweet = error_dict[error]
    api.update_status(tweet)
    return None


def media_tweet():
    api = get_api(2422730102)  # the user_id of @chessnutapp
    tweet = u"Uploading a file online @lordsheepy"
    fn = "https://www.google.com/images/srpr/logo11w.png"
    api.update_with_media(fn, status=tweet)
    return None
