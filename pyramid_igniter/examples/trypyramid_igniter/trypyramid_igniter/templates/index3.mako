<%inherit file='pyramid_igniter:/templates/master.bootstrap3.mako'/>

<%block name='title'>Try Pyramid-Igniter</%block>
<%block name='head_tail'>
    <link href='/static/theme.css' rel='stylesheet'>
    <link href='http://yandex.st/highlightjs/8.0/styles/github.min.css' rel='stylesheet'>
</%block>

<%block name='navbar_class'>navbar navbar-default navbar-fixed-top</%block>

<%block name='content'>
<div class='row center-block'>
    <div class='col-md-12 text-center'>
        <div class='row center-block'>
            <div class='col-md-4 text-center col-md-offset2'>
                <img src='http://trypyramid.com/static/images/pyramid_logo_on_transparent_background_222x213.png' width='222' height='213' alt='Pyramid'>
            </div>
            <div class='col-md-4 text-center'>
                <h1>&lt;- this picture</h1>
                <h3>has been stolen</h3>
                <h3>from the original site</h3>
                <h3><a href='http://trypyramid.com/'>http://trypyramid.com/</a></h3>
            </div>
        </div>
    </div>
</div><br />

<div class='row'>
<h3>Pyramid is easy to set up and use.</h3>

<h4>Install Python</h4>
<p>Install the Python interpreter from <a href="https://www.python.org/downloads/">Python.org</a>.</p>
<br />

<h4>Install Pyramid</h4>
<pre>
<code>&gt; pip install pyramid pyramid-igniter
&gt; pcreate -s starter trypyramid_igniter
&gt; cd trypyramid_igniter
&gt; python setup.py develop
</code>
</pre>
<br />

</div>

<div class='row'>
<h4>Create application __init__.py...</h4>
<pre>
<code>#encoding: utf-8

from pyramid.config import Configurator
from pyramid_igniter import Igniter, IgniterView, route


class Index(IgniterView):
    @route('/', renderer='trypyramid_igniter:/templates/index.jinja2')
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
</code></pre>

<br />
<h4>...template in /templates/index.jinja2</h4>
<pre>
<code>{&#37; extends 'pyramid_igniter:/templates/master.bootstrap3.jinja2' &#37;}

{&#37; block title &#37;}Try Pyramid-Igniter{&#37; endblock &#37;}
{&#37; block head_tail &#37;}
    &lt;link href='/static/theme.css' rel='stylesheet'&gt;
    &lt;link href='http://yandex.st/highlightjs/8.0/styles/github.min.css' rel='stylesheet'&gt;
{&#37; endblock &#37;}

{&#37; block navbar_class &#37;}navbar navbar-default navbar-fixed-top{&#37; endblock &#37;}

{&#37; block content &#37;}

    ...Deep recursion here...

{&#37; endblock &#37;}

{&#37; block tail &#37;}
    &lt;script src='http://yandex.st/highlightjs/8.0/highlight.min.js' type='text/javascript'>&lt;/script&gt;
    &lt;script type='text/javascript'&gt;
        $(document).ready(function() {
            hljs.initHighlightingOnLoad();
        });
    &lt;/script&gt;
{&#37; endblock &#37;}
</code></pre>
<br />
<h4>...style in /static/theme.css</h4>
<pre>
<code>html, body { height: 100%; }
body { padding: 90px 0 150px 0; }

.wrap { min-height: 100%; padding-bottom: 150px; }
* html .wrap { height: 100%; }

.footer { height: 131px; margin-top: -131px; }
.footer ul { padding: 0; }
.footer ul li { list-style: none; }
</code>
</pre>
</div><br />

<div class='row'>
<h4>Run your application</h4>
<pre><code>&gt; pserve development.ini</code></pre>
</div><br />

<div class='row'>
<h4>Open your application</h4>
<p>Visit the URL <a href='http://0.0.0.0:6543'>http://0.0.0.0:6543</a> in a web browser.</p>
</div><br /><br />

<div class='row'>
Wow! You got this site!<br />
P.S. Sorry for CDNs.<br />
P.P.S. There is no reason to use Pyramid for one-page static site, but why not?
</div>

</%block>

<%block name='tail'>
    <script src='http://yandex.st/highlightjs/8.0/highlight.min.js' type='text/javascript'></script>
    <script type='text/javascript'>
        $(document).ready(function() {
            hljs.initHighlightingOnLoad();
        });
    </script>
</%block>
