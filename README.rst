Pyramid-Igniter
===============
Translation and bug fix in progress.

As I said, almost all of my projects with Flask are combination of Flask-Classy and Flask-Admin.
Pyramid-Classy is already done. Main goal of Pyramid-Igniter is simplest way of creation 
administrative part of the web application, but...


Installation
------------
Install the extension with::

    $ pip install pyramid-igniter

or::

    $ easy_install pyramid-igniter


Let's see how it works
----------------------
.. code-block:: python

    # encoding: utf-8
    
    from pyramid.view import view_defaults
    from pyramid.config import Configurator
    from pyramid.httpexceptions import HTTPFound
    from pyramid_igniter import Igniter, IgniterView, route
    
    
    @view_defaults(renderer='/templates/index.jinja2')
    class Index(IgniterView):
        def index(self, request):  # /
            return dict(message='Some index page info')

        def cookie(self, request):  # /cookie
            response = self.render(request,
                                   'igniter_doc:/templates/index.jinja2',
                                   dict(message='Some index page info...'))
            response.set_cookie('test_cookie', 'test!')
            return response
    
    
    @view_defaults(renderer='/templates/pets.jinja2')
    class Pets(IgniterView):
        def index(self, request):
            pet_type = self.route_base.strip('/')
            return dict(message='Some info about %s' % pet_type, pet_type=pet_type)
    
    
    @view_defaults(renderer='/templates/message.jinja2')
    class BBS(IgniterView):
        def index(self, request):
            return dict(message='Some messages')
    
        @route('/add', renderer='/templates/message_add.jinja2')
        def add(self, request):
            if request.method == 'POST':
                return HTTPFound(request.route_path('bbs.success'))
            return {}
    
        @route('/success', renderer='/templates/message_success.jinja2')
        def success(self, request):
            return {}
    
    
    class Image(IgniterView):
        @route('/', renderer='/templates/image.jinja2')
        def index(self, request):
            return dict(message='Proof of concept')
    
    
    def main(global_config, **settings):
        config = Configurator(settings=settings)
        config.include('pyramid_jinja2')
        config.add_static_view('static', 'static', cache_max_age=3600)
    
        index = Igniter(config, Index('Project brand'), debug=True)
        index.add_view(Pets('Cats', route_base='/cats'), category='Pets')
        index.add_view(Pets('Dogs', route_base='/dogs'), category='Pets')
        index.add_view(BBS('Bulletin Board'))
        index.add_view(Image('Upload images'), visible=False)
        index.add_view(('Some link', '//github.com'))
    
        index.add_footer(('Item 1', '/url'), category='Some stuff')
        index.add_footer(('Item 2', '/url'), category='Some stuff')
        index.add_footer(('Item 3', '/url'), category='Some stuff')
        index.add_footer(('Job list', '/url'), category='Job')
        index.add_footer(('Add a resume', '/url'), category='Job')
        index.add_footer(('Facebook', '/url'), category='Social Networks')
        index.add_footer(('G+', '/url'), category='Social Networks')
        index.add_footer(('VK', '/url'), category='Social Networks')
    
        return config.make_wsgi_app()
        
This code will handle a list of URLs:

- /
- /cookie
- /cats/
- /dogs/
- /bbs/
- /bbs/add
- /bbs/success
- /image/


.. figure:: https://cloud.githubusercontent.com/assets/2255508/3421399/b97acbf4-feea-11e3-80f1-08b94d53ca0e.png
    :alt: /

.. figure:: https://cloud.githubusercontent.com/assets/2255508/3421398/b97a5ade-feea-11e3-8381-901204e45898.png
    :alt: /cats

.. figure:: https://cloud.githubusercontent.com/assets/2255508/3421401/b97ecace-feea-11e3-8be6-c5cb0e02958c.png
    :alt: /bbs

.. figure:: https://cloud.githubusercontent.com/assets/2255508/3421397/b977f6f4-feea-11e3-8b4f-75b998fe695d.png
    :alt: /bbs/add

.. figure:: https://cloud.githubusercontent.com/assets/2255508/3421396/b9751e34-feea-11e3-8d41-304e5148e986.png
    :alt: /bbs/success

.. figure:: https://cloud.githubusercontent.com/assets/2255508/3421400/b97cb6e4-feea-11e3-92d3-ab8d91ad1ac8.png
    :alt: /image/

.. figure:: https://cloud.githubusercontent.com/assets/2255508/3421395/b96024d4-feea-11e3-8bb3-d5fc5a0b8e94.png
    :alt: Footer


Well, in this short example you can see almost all the features of Pyramid-Igniter. It's an automatic creation of
menu items, footer items and pyramid routes. Simple, isn't it?


Handling views
**************
If you want to check something before proceeding the view in class, you can define a _handle_view(self, request) function.
This function should return a True or Response object (HTTPFound, HTTPForbidden etc.)
If you don't, there will be **no any** performance degradation.

.. code:: python

    def _handle_view(self, request):
        if request.path == '/admin/login':
            return True
        fail = HTTPFound(request.route_url('admin.login', return_to=request.path))
        request_cookie = request.cookies.get('signed')
        if not request_cookie:
            return fail


**Note** Be careful, _handle_view will be called before proceeding the view in all the functions of the class where this method
has been defined, even before HTTPFound if location is urls in the same class. Don't do the eternal loop ;-)


Important Notes
***************
Yes, (self, request).

The Index(IgniterView) class have route_base='/' by default.

The index(self, request) method handle root of the route_base by default. I mean, if route_base = '/admin' then 
index(self, request) will handle an ``/admin/`` url even without route decorator.

You can call classes right without defining ``route_base`` and these classes will handle a specified urls. 
I mean Help(IgniterView) will handle a ``/help/`` urls etc.

You can define debug flag (same way as route_base) to see routes and their names.

Same as Pyramid-Classy, all the functions with name starting with letter and defined in class 
IgniterView will handle a specified URL even without route decorator. For avoiding this you need to define a function with name starting with underscore _


Template blocks
---------------
There is four templates in this extensions for Mako and Jinja2. You need to extend one of this templates for properly work of this extension.

- master.bootstrap2.jinja2

- master.bootstrap3.jinja2

- master.bootstrap2.mako

- master.bootstrap3.mako

.. code:: python

    {% extends 'pyramid_igniter:/templates/master.bootstrap3.jinja2' %}

    {% block title %}Try Pyramid-Igniter{% endblock %}
    {% block head_tail %}
        <link href='/static/theme.css' rel='stylesheet'>
        <link href='http://yandex.st/highlightjs/8.0/styles/github.min.css' rel='stylesheet'>
    {% endblock %}

    {% block navbar_class %}navbar navbar-default navbar-fixed-top{% endblock %}

    {% block content %}
        Content
    {% endblock %}

    {% block tail %}
        <script type='text/javascript'>
            $(document).ready(function() {
                ...
            });
        </script>
    {% endblock %}


Blocks
******

- ``title`` Overwrite this block for the page title you need.

- ``head`` This block contains CDN-stylesheet for the bootstrap framework.

- ``head_tail`` This block might contain CSS and your scrtipts.

- ``navbar_class`` You can define the class for navbar you need. ``navbar navbar-default navbar-fixed-top`` for 100% width fixed navbar, for example.

- ``brand`` Block with the brand info. Don't you need this? Overwrite something like {% block brand %}{% endblock %} and you will not see project name.

- ``content`` The main block with content of your page.

- ``footer`` Footer block.

- ``tail_js`` This block contains scripts in the CDNs for bootstrap and jQuery. Overwrite it if you don't need this.

- ``tail`` Block for your JS-scripts and other.


Internationalization
--------------------
So damn long word. Aww, that's a hard way. And I mean not a pronunciation. Translation is job for template engine.

With Jinja2 it was easy but Mako want a lot of code. **I've decided do not do that**.

You can edit master.*.jinja2 files and replace every view.name to _(view.name), item.name to _(item.name) and child.name to _(child.name) 
and you will have your i18n with ~10% performance degradation in templating part.


Known Issues
------------
**First**. If you have added a tuple of (name, url) in add_view, then this menu will have class 'active' when you go to this url only. 
See example 'bash' in examples directory and check / and /page-2. This issue cannot be fixed without 
some heavy computations. Sad but true. There is some way to do the same thing with IgniterView classes.


**Second**. In example above title of the pages with URLs /cats and /dogs are the same: Project brand - Dogs.
I know the reason, but I cannot prove it. I hope you will use your own title instead of default value.


Both issues are not dead end, I guess.


Examples
--------
Github version contains two examples in the examples directory. It's a full-featured webapps.


API
---
.. code:: python

    Igniter(config, view, debug=False, footer_class='col-md-3')

- ``config`` is Pyramid Configuration instance.

- ``view`` is instance of IgniterView class.

- ``debug`` prints debug information about names and urls of the routes.

- ``footer_class``. By default uses `col-md-3` for Bootstrap3 grid. Use `span3` for the Bootstrap2.

- **Note**: the first view should be an IgniterClass instance with root route.

.. code:: python

    Igniter.add_view(self, view, visible=True, category=None)

- ``view`` is a tuple of (name, url) or the IngiterView instance.

- ``visible`` if visible=False, the item will not be shown in a menu.

- ``category`` is for dropdown menu of few items.


.. code:: python

    Igniter.add_footer(view, category=None)

- ``view`` is a tuple of (name, url) **only**. Sorry for that.

- ``category`` is a topic for footer items.


.. code:: python

    IgniterView(name=None, route_base=None)

- ``name`` is the name for menu item and page title.

- ``route_base`` is root url for the routes of this class. You can define it in class you write. All the routes of this class will use route_base for generating urls.


.. code:: python

    IgniterView.render(request, template, args)

- This method calls Pyramid render_to_response method. Don't forget that in that case **you need** use a full name of the template, including package name because it calls not in your class.

- ``template`` The renderer name used to perform the rendering, e.g. project:templates/page.jinja2.

- ``args`` is dict with arguments what you want render. Please don't use a variable named ``view``, it will be overwritten.


.. code:: python

    route(rule='/', **options)

- ``rule`` is the url which this function will serve. Multiple routes for single view also available.

- ``options`` takes exactly the same parameters as Pyramid's add_route, so you should feel free adding custom routes to any views you create.

- **Note** If you want to use Pyramid-Classy and Pyramid-Igniter both at the same time, you can import route from one of these extensions: they do exactly the same thing.


Changelog
*********

0.2.1
~~~~~

* Fixed a bug in assigning route_base variable.


0.2
~~~

* Added a method ``render`` to the IgniterView class. Rendering process needs some additional info about objects; now you can do some things more simpler.


0.1
~~~

Initial release.


Please feel free to contact me if you have any questions or comments.
