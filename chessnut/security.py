from pyramid.security import Allow, Everyone, Authenticated, ALL_PERMISSIONS
from .models import User


ADMINS = []


def groupfinder(userid, request):
    """callback for authentication policy"""
    if userid in ADMINS:
        return ['g:admins']
    else:
        return []


class Root(object):
    __acl__ = [
        (Allow, Authenticated, 'create'),
        (Allow, Everyone, 'view'),
        (Allow, 'g:admins', ALL_PERMISSIONS),
    ]

    def __init__(self, request):
        pass


class UserFactory(object):

    def __init__(self, request):
        self.request = request

    def __getitem__(self, key):
        user = User.get_by_username(key)
        user.__parent__ = self
        user.__name__ = key
        return user
