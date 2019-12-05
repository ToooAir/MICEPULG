from alchemyStart import engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    bind_id = Column('bind_id', String(4))
    line_user_id = Column('line_user_id', String(64))
    name = Column('name', String(10))
    email = Column('email', String(30))
    intro = Column('intro', Text)
    link = Column('link', Text)
    picture = Column('picture', String(64))


class UserDetail(Base):
    __tablename__ = 'user_detail'
    user_id = Column(Integer, ForeignKey(
        'user.id', ondelete='CASCADE'), primary_key=True)
    field_a = Column('Field_a', Text)
    field_b = Column('Field_b', Text)
    field_c = Column('Field_c', Text)


class Tags(Base):
    __tablename__ = 'tags'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    tag_name = Column('tag_name', String(10))
    tag_value = Column('Tag_value', String(20))


class Logs(Base):
    __tablename__ = 'logs'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    line_user_id = Column('line_user_id', String(64))
    comand = Column('comand', String(32))
    content = Column('content', Text)
    create_time = Column('create_time', Float)
    ip = Column('ip', String(40))
    spend_ms = Column('spend_ms', Integer)


class Followers(Base):
    __tablename__ = 'followers'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    line_user_id = Column('line_user_id', String(64))
    create_time = Column('create_time', Float)


Base.metadata.create_all(engine)
