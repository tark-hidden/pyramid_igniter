# encoding: utf-8
from markupsafe import Markup
import re

SECRET = 'It is a secret'
PER_PAGE = 20


def linebreaks(value):
    return re.sub('\r\n|\r|\n', Markup('<br />\n'), Markup.escape(value))


def timeformat(value, fmt):
    return value.strftime(fmt)
