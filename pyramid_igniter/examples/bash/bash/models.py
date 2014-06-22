# encoding: utf-8

from sqlalchemy import Column, Index, Integer, Text, SmallInteger
from sqlalchemy import DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

dbs = scoped_session(sessionmaker(extension=ZopeTransactionExtension(),
                                  expire_on_commit=False))
Base = declarative_base()


class QuoteModel(Base):
    __tablename__ = 'quotes'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    rating = Column(Integer)
    quote = Column(Text)


class AbyssModel(Base):
    __tablename__ = 'abyss'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    rating = Column(Integer)
    checked = Column(Boolean)
    quote = Column(Text)

    def __unicode__(self):
        return u'(%s, %s, %s, %s)' % (
            self.date, self.rating, self.checked, self.quote)


class StaffModel(Base):
    __tablename__ = 'staff'
    id = Column(Integer, primary_key=True)
    role = Column(Text)
    name = Column(Text)
    password = Column(Text)
    salt = Column(Text)


class InfoModel(Base):
    __tablename__ = 'info'
    id = Column(Integer, primary_key=True)
    count_quotes = Column(Integer)
    count_abyss = Column(Integer)
    per_page = Column(SmallInteger)

Index('quote_rating', QuoteModel.rating)
Index('abyss_rating', AbyssModel.rating)
Index('abyss_checked', AbyssModel.checked)
