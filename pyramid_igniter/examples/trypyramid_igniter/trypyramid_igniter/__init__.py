#encoding: utf-8

from pyramid.config import Configurator
from pyramid_igniter import Igniter, IgniterView, route


class Index(IgniterView):
    @route('/', renderer='trypyramid_igniter:/templates/index3.jinja2')
    def index(self, request):
        return {}


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    # config.include('pyramid_mako')  # do you like mako? Why?..
    config.add_static_view('static', 'static', cache_max_age=3600)

    docs = 'http://docs.pylonsproject.org'
    current_release = ('Current release', docs + '/projects/pyramid/en/latest/')
    dev_release = ('Development release', docs + '/projects/pyramid/en/master/')
    prev_release = ('Previous releases',
                    docs + '/en/latest/docs/pyramid.html#previous-versions')
    tour = ('Quick Tour', docs + '/projects/pyramid/en/latest/quick_tour.html')
    tutorials = ('Tutorials', docs + '/projects/pyramid-tutorials/en/latest/')
    quick_tutorial = ('Quick Tutorial', docs +
                      '/projects/pyramid/en/latest/quick_tutorial/index.html')
    cookbook = ('Cookbook', docs + '/projects/pyramid-cookbook/en/latest/')
    support = ('Support', docs + '/community/get-support')
    repository = ('Pyramid code repository',
                  'https://github.com/Pylons/pyramid')
    add_ons = ('Supported add-ons',
               docs + '/en/latest/docs/pyramid.html#supported-add-ons')

    # footer_class='span3'  # for Bootstrap2
    igniter = Igniter(config, Index('Try Pyramid-Igniter'))
    igniter.add_view(current_release, category='Documentation')
    igniter.add_view(dev_release, category='Documentation')
    igniter.add_view(prev_release, category='Documentation')
    igniter.add_view(tour, category='Documentation')
    igniter.add_view(tutorials, category='Learn')
    igniter.add_view(quick_tutorial, category='Learn')
    igniter.add_view(cookbook, category='Learn')
    igniter.add_view(support, category='Help')
    igniter.add_view(repository, category='Source')
    igniter.add_view(add_ons, category='Source')

    igniter.add_footer(current_release, category='Documentation')
    igniter.add_footer(dev_release, category='Documentation')
    igniter.add_footer(prev_release, category='Documentation')
    igniter.add_footer(tour, category='Documentation')
    igniter.add_footer(tutorials, category='Learn')
    igniter.add_footer(quick_tutorial, category='Learn')
    igniter.add_footer(cookbook, category='Learn')
    igniter.add_footer(support, category='Help')
    igniter.add_footer(repository, category='Source')
    igniter.add_footer(add_ons, category='Source')

    return config.make_wsgi_app()
