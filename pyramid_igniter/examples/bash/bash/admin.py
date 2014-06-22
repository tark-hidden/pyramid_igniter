# encoding: utf-8
from pyramid_igniter import IgniterView, route


class Admin(IgniterView):
    @route('/')
    def index(self):
        pass
