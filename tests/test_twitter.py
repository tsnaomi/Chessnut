import unittest
import chessnut.twitter as twitter
# from pyramid import testing
# from paste.deploy.loadwsgi import appconfig

# from webtest import TestApp
# from mock import Mock

# from sqlalchemy import engine_from_config
# from sqlalchemy.orm import sessionmaker
# from app.db import Session
# from app.db import Entity  # base declarative object
# from app import main
# import os

# here = os.path.dirname(__file__)
# settings = appconfig('config:' + os.path.join(here, '../../', 'test.ini'))


# class BaseTestCase(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         cls.engine = engine_from_config(settings, prefix='sqlalchemy.')
#         cls.Session = sessionmaker()

#     def setUp(self):
#         connection = self.engine.connect()

#         # begin a non-ORM transaction
#         self.trans = connection.begin()

#         # bind an individual Session to the connection
#         Session.configure(bind=connection)
#         self.session = self.Session(bind=connection)
#         Entity.session = self.session

#     def tearDown(self):
#         # rollback - everything that happened with the
#         # Session above (including calls to commit())
#         # is rolled back.
#         testing.tearDown()
#         self.trans.rollback()
#         self.session.close()


class TweetHandlingTests(unittest.TestCase):

    # def setUp(self):
    #     self.config = testing.setUp(request=testing.DummyRequest())
    #     super(TweetHandlingTests, self).setUp()

    def test_move_true(self):
        inp_dict = {
            'opponent': 'opponent',
            'game': 'game',
            'move': 'move',
            'message': 'message goes here'
        }
        move = twitter.is_move(inp_dict)
        self.assertEqual(move, True)

    def test_move_false(self):
        inp_dict = {
            'opponent': 'opponent',
            'game': 'game',
            'move': '',
            'message': ''
        }
        move = twitter.is_move(inp_dict)
        self.assertEqual(move, False)

    def test_challenge_valid(self):
        inp_dict = {
            'opponent': 'opponent',
            'game': 'game',
            'move': '',
            'message': ''
        }
        challenge = twitter.is_challenge(inp_dict)
        self.assertEqual(challenge, True)

    def test_challenge_or_accept(self):
        # needs db access
        pass

    def test_accept(self):
        # needs db access
        pass

    def test_name_taken(self):
        # needs db access
        pass


if __name__ == '__main__':
    unittest.main()
