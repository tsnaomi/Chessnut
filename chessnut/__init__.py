from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from social.apps.pyramid_app.models import init_social
from pyramid.security import (
    authentication_policy,
    authorization_policy,
    )

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings,
                          authentication_policy=authentication_policy,
                          authorization_policy=authorization_policy,
                          root_factory=Root,)

    # python social auth
    config.include('social.apps.pyramid_app')
    config.scan('social.apps.pyramid_app')
    init_social(config, Base, DBSession)

    # views
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.scan()
    return config.make_wsgi_app()
