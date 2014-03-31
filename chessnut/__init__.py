from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from social.apps.pyramid_app.models import init_social
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from .models import (
    DBSession,
    Base,
    )

from .security import (
    Root,
    # UserFactory,
    # GameFactory,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    authentication_policy = AuthTktAuthenticationPolicy('somesecret')
    authorization_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings,
                          authentication_policy=authentication_policy,
                          authorization_policy=authorization_policy,
                          root_factory=Root,)
    config.add_jinja2_search_path("chessnut:templates")

    # python social auth
    # config.include('social.apps.pyramid_app')
    # config.include('pyramid_jinja2')
    # config.scan('social.apps.pyramid_app')
    # init_social(config, Base, DBSession)

    # views
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('index', '/index')
    config.add_route('register', '/register')
    config.scan()
    return config.make_wsgi_app()
