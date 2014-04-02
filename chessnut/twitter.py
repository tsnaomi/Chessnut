from .models import (
    DBSession,
    TwUser,
    Game
    )
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
    tweet = tweet.encode()

    match = re.match(
        r'^@\w{11} (@(?P<opponent>[^\s]+) )?#(?P<game>\w+) (?P<move>[^\s]+) (?P<message>.*)$',
        tweet
    )

    if match:
        return match.groupdict()
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
    for i in range(size):
        move = movequeue.get()
        move, user = move.text, move.user.id
        parsed = tweet_parser(move)
        if not parsed['move']:

        try:
            game = Game.get_by_name(game)
            game_update = cg(game.pgn)
            game_update(move)
            game.pgn = game_update.pgn
            image_url = generate_image(cg.image_string)
            send_tweet(user, image_url, game)
        except:
            send_error(move, game)
    return None


def send_tweet(user, gamename, image_url):
    api = get_api(user)
    opponent = u'lordsheepy'
    tweet = "@%s Gamename: %s Boardstate: %s" % (opponent, gamename, image_url)
    api.update_status(tweet)
    return


def send_error(user, gamename):
    api = get_api(2422730102)  # the user_id of @chessnutapp
    user = api.get_user(user)
    user = user.screen_name
    tweet = "@%s your last move had some errors, buddy" % user
    api.update_status(tweet)
    return None


def media_tweet():
    api = get_api(2422730102)  # the user_id of @chessnutapp
    tweet = "Uploading a file online @lordsheepy"
    fn = "https://www.google.com/images/srpr/logo11w.png"
    api.update_with_media(fn, status=tweet)
    return None
