import tweepy
from celery.task import task
from paste.deploy.loadwsgi import appconfig
from chessnut.twitter import tweet_recv

config = appconfig('config:development.ini', 'main', relative_to='.')

consumer_key = config['consumer_key']
consumer_secret = config['consumer_secret']


class CnStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        tweet_recv.delay(status)

    def on_disconnect():
        pass


def streaming_api(track):
    key = "15854617-VGEdtlUwd4AgCRpUdntQxmAEnb1Xn7mfNyyl8BRGF"
    secret = "AZVnbiJ3XjoMHdc20ZcDAyxLqpFGbM6sHDymJfDEMRMFh"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(key, secret)
    stream = tweepy.Stream(auth, CnStreamListener(), timeout=90)
    stream.filter(track=track)


if __name__ == '__main__':
    streaming_api(["#chessnut"])

