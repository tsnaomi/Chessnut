from .models import (
    DBSession,
    TwUser,
    )
import tweepy




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
        move, gamename = parse_move(move)
        try:
            board = make_move(move)
            image_url = generate_image(board)
            send_tweet(user, image_url, gamename)
        except:
            send_error(move, gamename)
    return None


def send_tweet(user, gamename, image_url):
    api = get_api(user)
    opponent = u'lordsheepy'
    tweet = "@%s Gamename: %s Boardstate: %s" % (opponent, gamename, image_url)
    api.update_status(tweet)
    return


def send_error(user, gamename):
    api = get_api(2422730102) # the user_id of @chessnutapp
    user = api.get_user(user)
    user = user.screen_name
    tweet = "@%s your last move had some errors, buddy" % user
    api.update_status(tweet)
    return None
