import unittest
from tweet_parser import tweet_parser


class TestTweetParser(unittest.TestCase):
    """Test the tweet parser."""
    def setUp(self):
        self.good_tweet = u'@ChessnutApp #bobisgoingdown Nb2c3+ suck it bob'
        self.bad_tweet = u'@ChessnutApp gamewithouthashtag message some move'
        self.expected = {
            'game': 'bobisgoingdown',
            'move': 'Nb2c3+',
            'message': 'suck it bob',
        }

    def test_good_tweet(self):
        groups = tweet_parser(self.good_tweet)
        for key in self.expected:
            self.assertEqual(self.expected[key], groups[key])

    def test_bad_tweet(self):
        self.assertRaises(ValueError, tweet_parser, self.bad_tweet)


if __name__ == '__main__':
    unittest.main()
