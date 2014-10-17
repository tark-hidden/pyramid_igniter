# encoding: utf-8

import inspect
from functools import wraps
from pyramid.renderers import render_to_response
from re import sub


def route(rule='/', **options):
    def decorator(f):
        if not hasattr(f, 'rules'):
            f.rules = []
        f.rules.append((rule, options))
        return f
    return decorator


def wrap_view(f):
    @wraps(f)
    def inner(request):
        abort = inner._handle_view(request)
        if abort is not True:
            return abort
        return f(request)
    return inner


def prettify_name(name):
    return sub(r'(?<=.)([A-Z])', r' \1', name)


def get_members(base, current):
    base_members = dir(base)
    all_members = inspect.getmembers(current, predicate=inspect.ismethod)
    return [member for member in all_members
            if not member[0] in base_members and not member[0].startswith('_')]


class Inner(object):
    __slots__ = ('igniter', 'name')


class Igniter(object):
    url = ''
    brand = ''

    def __init__(self, config, view, debug=False, footer_class='col-md-3'):
        self.config = config
        self.route_base = view.route_base.rstrip('/')
        self.menu = []
        self.menu_categories = {}
        self.footer = []
        self.footer_categories = {}
        self.debug = debug
        self.footer_class = footer_class
        self.add_view(view)

    def add_view(self, view, visible=True, category=None):
        if isinstance(view, tuple) and visible:  # who can choose False?
            name, url = view
            self.add_to_menu(name, url, [], category, True)
            return

        base = self.route_base if view.route_base != self.route_base else ''
        name, url, views = view.get_views(self)
        if not self.brand:
            self.brand = name
        if not self.url:
            self.url = url
        if visible and self.url != url:
            self.add_to_menu(name, self.build_url(base, url), views, category)

        for current_view in views:
            route_name, url, function, options = current_view
            url = self.build_url(base, url)
            function.func_dict['igniter'] = self
            function.func_dict['name'] = name
            self.config.add_route(route_name, url)
            self.config.add_view(function, route_name=route_name, **options)
            if self.debug:
                print "%s => '%s'" % (url, route_name)

    def add_to_menu(self, name, url, views, category=None, is_link=False):
        if category:
            if category not in self.menu_categories:
                self.menu_categories[category] = []
                self.menu.append(dict(name=category, url=None, is_link=is_link))
            self.menu_categories[category].append(dict(name=name, url=url))
            return
        children = {view[0] for view in views}  # very fast set
        self.menu.append(dict(name=name, url=url, is_link=is_link,
                              children=children))

    def add_footer(self, view, category=None):
        if not isinstance(view, tuple):
            raise TypeError('The footer item should be a tuple (name, url)')
        name, url = view
        if category:
            if category not in self.footer_categories:
                self.footer_categories[category] = []
                self.footer.append(dict(name=category, url=None))
            self.footer_categories[category].append(dict(name=name, url=url))
            return
        self.footer.append(dict(name=name, url=url))

    @staticmethod
    def build_url(base, url):
        return '%s%s' % (base, url)

    def is_active(self, request, item):
        if item['is_link']:  # check only giving url
            return request.matched_route.path == self.route_base + item['url']
        return request.matched_route.name in item['children']


class IgniterView(object):
    route_base = '/'
    igniter = None
    __view_defaults__ = {}

    def __init__(self, name=None, route_base=None):
        n = self.__class__.__name__
        self.name = name or prettify_name(n)
        prefix = n.lower()
        self.prefix = prefix
        if not route_base:
            if self.route_base == '/':
                self.route_base = '' if prefix == 'index' else '/%s' % prefix
        elif route_base == '/':
            self.route_base = ''
        else:
            self.route_base = '/%s' % route_base.strip('/')
            self.prefix = route_base.strip('/')

    def get_views(self, igniter):
        if not self.igniter:
            self.igniter = igniter

        views = []
        is_handle_view = hasattr(self, '_handle_view')
        for name, _ in get_members(IgniterView, self):
            view_defaults = self.__view_defaults__.copy()
            route_name = '%s.%s' % (self.prefix, name)
            options = view_defaults
            url = self.build_url(name, name)
            attr = getattr(self, name)
            if hasattr(attr, 'rules'):
                for idx, (url, options) in enumerate(attr.rules):
                    url = self.build_url(name, url)
                    route_name = options.pop('route_name', None)
                    route_name_orig = route_name
                    view_defaults = self.__view_defaults__.copy()
                    view_defaults.update(options or {})
                    options = view_defaults
                    if not route_name:
                        route_name = '%s.%s' % (self.prefix, name)
                    if not route_name_orig and len(attr.rules) > 1:
                        route_name = '%s_%d' % (route_name, idx)
                    if is_handle_view:
                        attr = wrap_view(attr)
                        attr.func_dict['_handle_view'] = self._handle_view
                    views.append((route_name, url, attr, options))
            else:
                if is_handle_view:
                    attr = wrap_view(attr)
                    attr.func_dict['_handle_view'] = self._handle_view
                views.append((route_name, url, attr, options))
        return self.name, self.route_base + '/', views

    def build_url(self, name, url=''):
        if name == 'index' and url == name:
            url = ''
        return '%s/%s' % (self.route_base, url.lstrip('/'))

    def render(self, request, template, args=None):
        Inner.igniter = self.igniter
        Inner.name = self.name
        args = args or {}
        args['view'] = Inner
        return render_to_response(template, args, request=request)
