from alchemyStart import engine

from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    bind_id = Column('bind_id', String(4))
    line_user_id = Column('line_user_id', String(64), unique=True)
    name = Column('name', String(20))
    email = Column('email', String(100))
    intro = Column('intro', Text)
    link = Column('link', Text)
    picture = Column('picture', String(128))
    comment = relationship("Comment", backref="user", lazy='dynamic',
                           cascade='all, delete-orphan', passive_deletes=True)
    qrcode = Column('qrcode', String(32))


class UserDetail(Base):
    __tablename__ = 'user_detail'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(
        'user.id', ondelete='CASCADE'))
    field_a = Column('field_a', Text)
    field_b = Column('field_b', Text)
    field_c = Column('field_c', Text)
    field_d = Column('field_d', Text)
    field_e = Column('field_e', Text)


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
    create_time = Column('create_time', Integer)
    ip = Column('ip', String(40))
    spend_ms = Column('spend_ms', Integer)


class Followers(Base):
    __tablename__ = 'followers'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    line_user_id = Column('line_user_id', String(64))
    create_time = Column('create_time', Integer)


class Comment(Base):
    __tablename__ = 'comment'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    create_time = Column('create_time', Integer)
    sender = Column('sender', String(64), ForeignKey(
        'user.line_user_id', ondelete="CASCADE"))
    receiver = Column('receiver', String(64))
    content = Column('content', Text)


Base.metadata.create_all(engine)
