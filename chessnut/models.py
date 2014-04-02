# import sqlalchemy as sa
from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    DateTime,
    ForeignKey,
    BigInteger,
    )

from sqlalchemy.ext.declarative import declarative_base

from pyramid.security import (
    ALL_PERMISSIONS,
    DENY_ALL,
    Allow,
    Everyone)

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    # relationship,
    synonym,
    )

from zope.sqlalchemy import ZopeTransactionExtension
import datetime
import cryptacular.bcrypt


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

crypt = cryptacular.bcrypt.BCRYPTPasswordManager()


def hash_password(password):
    return unicode(crypt.encode(password))


class User(Base):

    @property
    def __acl__(self):
        return [
            (Allow, self.id, 'edit'),
            (Allow, 'g:admins', ALL_PERMISSIONS),
            (Allow, Everyone, DENY_ALL)
        ]

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(Unicode(20), unique=True)
    email = Column(Unicode(50))
    _password = Column('password', Unicode(60))

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = hash_password(password)

    password = property(_get_password, _set_password)
    password = synonym('_password', descriptor=password)

    def __init__(self, username, password, email):
        self.username = username
        self.email = email
        self.password = password

    @classmethod
    def get_by_username(cls, username):
        return DBSession.query(cls).filter(cls.username == username).first()

    @classmethod
    def check_password(cls, username, password):
        user = cls.get_by_username(username)
        if not user:
            return False
        return crypt.check(user.password, password)


class TwUser(Base):
    __tablename__ = 'twuser'
    id = Column(Integer, primary_key=True)
    key = Column(Unicode(80))
    secret = Column(Unicode(80))
    user_id = Column(BigInteger)

    def __init__(self, key, secret, user_id):
        self.key = key
        self.secret = secret
        self.user_id = user_id

    @classmethod
    def get_by_id(cls, id):
        return DBSession.query(cls).filter(cls.id == id).first()

    @classmethod
    def get_by_secret(cls, secret):
        return DBSession.query(cls).filter(cls.secret == secret).first()

    @classmethod
    def get_by_user_id(cls, user_id):
        return DBSession.query(cls).filter(cls.user_id == user_id).first()


class Game(Base):
    __tablename__ = 'game'
    game_id = Column(Integer, primary_key=True)
    owner = Column(Integer, ForeignKey('users.id'), nullable=False)
    opponent = Column(Integer, ForeignKey('users.id'), nullable=False)

    @property
    def __acl__(self):
        return [
            (Allow, self.owner, 'edit'),
            (Allow, 'g:admins', ALL_PERMISSIONS),
            (Allow, Everyone, 'view'),
            ]

    @classmethod
    def get_by_gameid(cls, game_id):
        return DBSession.query(cls).filter(cls.game_id == game_id).first()


class SinceId(Base):
    __tablename__ = 'since_id'
    id = Column(Integer, primary_key=True)
    value = Column(BigInteger)

    def __init__(self, value):
        self.value = value

    @classmethod
    def get_by_id(cls, id):
        return DBSession.query(cls).filter(cls.id == id).first()
