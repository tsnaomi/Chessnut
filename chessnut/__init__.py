from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid_beaker import session_factory_from_settings
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
    session_factory = session_factory_from_settings(settings)
    consumer_key = settings.get('consumer_key', '')
    consumer_secret = settings.get('consumer_secret', '')
    settings['consumer_key'] = consumer_key
    settings['consumer_secret'] = consumer_secret
    config = Configurator(settings=settings,
                          authentication_policy=authentication_policy,
                          authorization_policy=authorization_policy,
                          root_factory=Root,
                          )
    config.set_session_factory(session_factory)
    # jinja 2 config
    config.add_jinja2_search_path("chessnut:templates")
    config.include('pyramid_jinja2')

    # views
    config.add_static_view('static', 'static', cache_max_age=3600)
    # config.add_route('front', '/front')
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('twauth', '/twauth')
    config.add_route('moves', '/moves')
    # config.add_route('index', '/index')
    # config.add_route('register', '/register')
    # config.add_route('mentions', '/mentions')
    config.add_route('list', '/matches/{id:\d+}')
    config.add_route('match', '/match/{name:\w+}')
    config.add_route('notation', '/notation')
    config.scan()
    return config.make_wsgi_app()
