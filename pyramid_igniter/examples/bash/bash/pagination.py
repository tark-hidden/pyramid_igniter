# encoding: utf-8

import math
from markupsafe import Markup


class Pagination(object):
    """ https://github.com/tark-hidden/pagination
    """
    def __init__(self, initial_path, path, count, per_page, page=1, window=10):
        self.count = count
        self.page = page
        self.per_page = per_page
        self.initial_path = initial_path
        self.path = path
        self.window = window

        items = []
        if self.count > self.per_page:
            last_page = 0
            p = self.page
            total = int(math.ceil(float(self.count) / self.per_page))
            if total <= self.window:
                pages = range(1, total + 1)
            else:
                pages = sorted(
                    set(range(1, 4)) |
                    set(range(max(1, p - 2), min(p + 3, total + 1))) |
                    set(range(total - 2, total + 1)))
            for page in pages:
                if page != last_page + 1:
                    items.append(('#', '...'))
                if page == 1:
                    path = self.initial_path
                else:
                    path = self.path.format(page=page)
                items.append((path, page))
                last_page = page
        self._items = items

    def items(self):
        return self._items

    def links(self):
        items = []
        p = self.page
        for url, page in self._items:
            if url == '#':
                items.append("<li class='disabled'><a href='#'>...</li>")
                continue
            items.append("<li%s><a href='%s'>%d</a></li>" % (
                ' class="active"' if page == p else '', url, page))

        return Markup(''.join(items))
