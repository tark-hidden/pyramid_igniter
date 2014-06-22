# encoding: utf-8

from pyramid.config import Configurator
from pyramid_igniter import Igniter
from sqlalchemy import engine_from_config
from views import Index, Admin, Moderation
from models import dbs, Base


def main(global_config, **settings):
    engine = engine_from_config(settings, 'sqlalchemy.')
    dbs.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)

    index = Igniter(config, Index('Quotes'), debug=True)
    index.add_view(('New quotes', '/'))
    index.add_view(('Random', '/random'))
    index.add_view(('Best', '/best'))
    index.add_view(('Abyss', '/abyss'))
    index.add_view(('Abyss best', '/abyss-best'))
    index.add_view(('Add', '/add'))

    admin = Igniter(config, Admin('Quotes Administration'), debug=True)
    admin.add_view(Moderation())
    admin.add_view(('Logout', '/admin/logout'))

    return config.make_wsgi_app()
