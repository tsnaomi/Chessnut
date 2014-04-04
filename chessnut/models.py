from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    UnicodeText,
    ForeignKey,
    BigInteger,
    Boolean
    )

from sqlalchemy.ext.declarative import declarative_base

from pyramid.security import (
    ALL_PERMISSIONS,
    Allow,
    Everyone)

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class TwUser(Base):
    __tablename__ = 'twuser'
    id = Column(Integer, primary_key=True)
    key = Column(Unicode(80))
    secret = Column(Unicode(80))
    user_id = Column(BigInteger)
    user_sn = Column(Unicode(16))

    def __init__(self, key, secret, user_id, user_sn):
        self.key = key
        self.secret = secret
        self.user_id = user_id
        self.user_sn = user_sn

    @classmethod
    def get_by_id(cls, id):
        return DBSession.query(cls).filter(cls.id == id).first()

    @classmethod
    def get_by_secret(cls, secret):
        return DBSession.query(cls).filter(cls.secret == secret).first()

    @classmethod
    def get_by_user_id(cls, user_id):
        return DBSession.query(cls).filter(cls.user_id == user_id).first()


class Challenge(Base):
    __tablename__ = 'challenge'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(50), nullable=False, unique=True)
    owner = Column(Integer, ForeignKey('twuser.id'), nullable=False)
    owner_sn = Column(Unicode(50), nullable=False)
    opponent = Column(Unicode(50), nullable=False)
    opponent_id = Column(Integer, ForeignKey('twuser.id'), nullable=True)

    def __init__(self, name, owner, opponent, owner_sn):
        self.name = name
        self.owner = owner
        self.owner_sn = owner_sn
        self.opponent = opponent

    def accept(self, opponent):
        self.opponent_id = opponent
        game = Game(self)
        DBSession.add(game)
        return None

    @classmethod
    def get_by_name(cls, name):
        return DBSession.query(cls).filter(cls.name == name).first()


class Game(Base):
    __tablename__ = 'game'
    game_id = Column(Integer, primary_key=True)
    name = Column(Unicode(50))
    owner = Column(Integer, ForeignKey('twuser.id'),
                   nullable=False)
    opponent = Column(Integer, ForeignKey('twuser.id'),
                      nullable=False)
    pgn = Column(UnicodeText)
    boards = Column(UnicodeText)
    turn = Column(Integer)
    is_over = Column(Boolean)
    is_winner = Column(Integer, ForeignKey('twuser.id'), nullable=True)

    def __init__(self, challenge):
        self.name = challenge.name
        self.owner = int(challenge.owner)
        self.opponent = int(challenge.opponent_id)
        self.pgn = u''
        self.boards = u''
        self.turn = self.owner
        self.is_over = False

    def is_turn(self, player):
        if player == self.turn:
            return True
        return False

    def end_turn(self):
        if self.turn == self.owner:
            self.turn = self.opponent
            return True
        elif self.turn == self.opponent:
            self.turn = self.owner
            return True
        return False

    def get_boards(self):
        BOARDS = []
        boards = self.boards[:-1].split(' ')
        for board in boards:
            BOARDS.append('/static/boards/%s.png' % board)
        return BOARDS

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

    @classmethod
    def get_by_name(cls, name):
        return DBSession.query(cls).filter(cls.name == name).first()

    @classmethod
    def get_by_person(cls, user_id):
        games = DBSession.query(cls).filter(cls.owner == user_id).all()
        games.extend(DBSession.query(cls).filter(
                     cls.opponent == user_id).all())
        return games


class SinceId(Base):
    __tablename__ = 'since_id'
    id = Column(Integer, primary_key=True)
    value = Column(BigInteger)

    def __init__(self, value):
        self.value = value

    @classmethod
    def get_by_id(cls, id):
        return DBSession.query(cls).filter(cls.id == id).first()
