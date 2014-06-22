# encoding: utf-8

import re
import time
import random
import datetime
import transaction
from hashlib import sha256
from pyramid.session import signed_serialize, signed_deserialize
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_defaults
from sqlalchemy import func
from pyramid_igniter import IgniterView, route
from filters import SECRET, PER_PAGE
from pagination import Pagination
from models import dbs, QuoteModel, AbyssModel, StaffModel


@view_defaults(renderer='/index.jinja2', http_cache=0)
class Index(IgniterView):
    def _random(self, min_id, max_id, amount):
        return [random.randint(min_id, max_id) for _ in range(amount)]

    @route('/')
    @route('/page-{page:\d+}')
    def index(self, request):
        page = int(request.matchdict.get('page', 1))
        count = dbs.query(func.count(QuoteModel.id)).scalar()
        quotes = dbs.query(QuoteModel).order_by(QuoteModel.id.desc())\
            .offset((page - 1)*PER_PAGE)\
            .limit(PER_PAGE).all()

        # this takes ~0.05 ms on my low-budget computer and have a nice URL.
        t = time.clock()
        pagi = Pagination(initial_path='/',
                          path='/page-{page}',
                          window=10,
                          # count=2500,
                          # per_page=20,
                          count=count,
                          per_page=PER_PAGE,
                          page=page).links()
        print (time.clock() - t)*1000, 'ms'
        # this takes 1.7 ms on my low-budget computer and URL is bad.
        # url_for_page = PageURL('/', dict(page=page))
        # current_page = paginate.Page(
        #     quotes, page, items_per_page=PER_PAGE, url=url_for_page)
        # pagi = current_page.pager(format='$link_first ~3~ $link_last')
        return dict(quotes=quotes, pagination=pagi)

    @route('/{id:\d+}', route_name='quote.get')
    def get(self, request):
        quotes = []
        quote_id = int(request.matchdict['id'])
        quote = dbs.query(QuoteModel).get(quote_id)
        if quote:
            quotes.append(quote)
        return dict(quotes=quotes)

    @route('/{id:\d+}/{action}', renderer='json')
    def action(self, request):
        quote_id = int(request.matchdict['id'])
        action = request.matchdict['action']
        quote = dbs.query(QuoteModel).get(quote_id)
        if quote:
            quote.rating += 1 if action == 'rulez' else -1
            transaction.commit()
            if request.is_xhr:
                return dict(rating=quote.rating)
            return HTTPFound(request.route_url('quote.get', id=quote_id))
        return dict(error='Quote not found')

    def random(self, request):
        min_id = dbs.query(QuoteModel).order_by(QuoteModel.id).first().id
        max_id = dbs.query(QuoteModel).order_by(QuoteModel.id.desc()).first().id
        ids = self._random(min_id, max_id, 20)
        quotes = dbs.query(QuoteModel).filter(QuoteModel.id.in_(ids)).all()
        random.shuffle(quotes)
        return dict(quotes=quotes)

    @route('/best')
    @route('/best/page-{page:\d+}')
    def best(self, request):
        page = int(request.matchdict.get('page', 1))
        count = dbs.query(func.count(QuoteModel.id)).scalar()
        pagi = Pagination(initial_path='/best',
                          path='/best/page-{page}',
                          window=10,
                          count=count,
                          per_page=PER_PAGE,
                          page=page).links()
        quotes = dbs.query(QuoteModel)\
            .order_by(QuoteModel.rating.desc())\
            .offset((page - 1) * PER_PAGE)\
            .limit(PER_PAGE).all()
        return dict(quotes=quotes, pagination=pagi)

    @route('/abyss', renderer='/abyss.jinja2')
    def abyss(self, request):
        min_id = dbs.query(AbyssModel).order_by(AbyssModel.id).first().id
        max_id = dbs.query(AbyssModel).order_by(AbyssModel.id.desc()).first().id
        ids = set(self._random(min_id, max_id, PER_PAGE + 20))
        quotes = dbs.query(AbyssModel)\
            .filter(AbyssModel.id.in_(ids))\
            .limit(PER_PAGE).all()
        random.shuffle(quotes)
        return dict(quotes=quotes)

    @route('/abyss/{id:\d+}/{action}', renderer='json')
    def abyss_action(self, request):
        quote_id = int(request.matchdict['id'])
        action = request.matchdict['action']
        quote = dbs.query(AbyssModel).get(quote_id)
        if quote:
            quote.rating += 1 if action == 'rulez' else -1
            transaction.commit()
            if request.is_xhr:
                return dict(rating=quote.rating)
        return HTTPFound('/abyss')

    @route('/abyss-best', renderer='/abyss.jinja2')
    def abyss_best(self, request):
        quotes = dbs.query(AbyssModel).order_by(
            AbyssModel.rating.desc()).limit(PER_PAGE).all()
        return dict(quotes=quotes)

    @route('/add', renderer='/add.jinja2')
    def add(self, request):
        if request.method == 'POST':
            email = request.POST.get('email')
            quote = request.POST.get('quote', '').strip('\r\n ')
            quote_len_wo_spaces = len(re.sub('\s+', '', quote))
            if quote_len_wo_spaces < 50:
                return dict(quote=quote, message='Quote is too short.')
            elif quote_len_wo_spaces > 1000:
                return dict(quote=quote, message='Quote is too long.')
            elif quote.count('\n') > 50:
                return dict(quote=quote, message='Quote is too wide. '
                            'Do you really need so many lines?')
            if not email:  # simple anti-spam protection, LOL
                date = datetime.datetime.utcnow()
                dbs.add(
                    AbyssModel(date=date, rating=0, checked=False, quote=quote))
                transaction.commit()
            return HTTPFound('/add/success')
        return {}

    @route('/add/success', renderer='/add.jinja2')
    def add_success(self, request):
        return dict(message='Quote has been added in Abyss successfully.')


@view_defaults(http_cache=0)
class AdminView(IgniterView):
    def _handle_view(self, request):
        if request.path == '/admin/login':
            return True
        fail = HTTPFound(request.route_url('admin.login', url=request.path))
        request_cookie = request.cookies.get('signed')
        if not request_cookie:
            return fail

        cookie = signed_deserialize(request_cookie, SECRET)
        login = cookie.get('time')
        return True if login else fail


class Admin(AdminView):
    """ I don't want to use a Pyramid ACL and session factory. Sorry.
    """
    route_base = '/admin'

    @route('/', renderer='/admin/index.jinja2')
    def index(self, request):
        quote_count = dbs.query(QuoteModel).count()
        # abyss_count = dbs.query(AbyssModel).count()
        abyss_count = dbs.query(AbyssModel).filter_by(checked=0).count()
        return dict(quote_count=quote_count, abyss_count=abyss_count)

    @route('/login', renderer='/admin/login.jinja2')
    def login(self, request):
        if request.method == 'POST':
            login = request.POST.get('login')
            password = request.POST.get('password')
            if login and password:
                user = dbs.query(StaffModel).filter_by(name=login).first()
                if user and user.password == sha256(
                        password + user.salt).hexdigest():
                    now = datetime.datetime.utcnow()
                    csrf = sha256(str(now)).hexdigest()
                    val = signed_serialize({'time': now, 'csrf': csrf}, SECRET)
                    response = HTTPFound(request.route_url('admin.index'))
                    response.set_cookie('signed', val)
                    return response
                return dict(
                    error='Something went wrong. Try "admin" and "111111"')
        return {}

    @route('/logout', renderer='/admin/logout.jinja2')
    def logout(self, request):
        request_cookie = request.cookies.get('signed')
        if not request_cookie:
            return {}
        cookie = signed_deserialize(request_cookie, SECRET)
        cookie_csrf = cookie.get('csrf')
        if request.method == 'POST':
            csrf = request.POST.get('csrf')
            if csrf == cookie_csrf:
                response = HTTPFound(request.route_url('admin.index'))
                response.delete_cookie('signed')
                return response
        return dict(csrf=cookie_csrf)


class Moderation(AdminView):
    def _get_cookie(self, request):
        request_cookie = request.cookies.get('signed')
        if not request_cookie:
            return {}
        return signed_deserialize(request_cookie, SECRET)

    @route('/', renderer='/admin/moderation.jinja2')
    def index(self, request):
        quotes = dbs.query(AbyssModel).filter_by(
            checked=0).limit(PER_PAGE).all()
        csrf = self._get_cookie(request).get('csrf')
        return dict(quotes=quotes, csrf=csrf)

    @route('/{quote_id:\d+}/{csrf}', renderer='string')
    def action(self, request):
        quote_id = int(request.matchdict['quote_id'])
        csrf = request.matchdict['csrf']
        cookie_csrf = self._get_cookie(request).get('csrf')
        if cookie_csrf and cookie_csrf == csrf and quote_id:
            action = request.POST.get('action')
            quote = dbs.query(AbyssModel).get(quote_id)
            if not quote:
                return 'no quote'  # who cares?

            if action == 'approve':
                body = request.POST.get('body', '')  # quote has been edited?
                quote_body = body if body else quote.quote
                # copy (not move) in QuoteModel
                dbs.add(QuoteModel(date=quote.date,
                                   rating=quote.rating,
                                   quote=quote_body))
                # and checked=1 in AbyssModel. The quote still exists in Abyss
                quote.checked = 1
                transaction.commit()
            elif action == 'refuse':
                quote.checked = 1
                transaction.commit()
            elif action == 'delete':
                dbs.delete(quote)
                dbs.flush()
            return 'ok'
        return 'fail'  # returned value means nothing
