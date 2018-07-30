# coding: utf-8
import os
from datetime import timedelta

basedir = os.path.dirname(os.path.abspath(__file__))


class Config(object):
    # Flask config
    SECRET_KEY = '^dhfU*W#Sds12:>C'
    PER_PAGE = 10
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    USE_SESSION_FOR_NEXT = True
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=10)
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data', 'blog.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data', 'blog.sqlite')

config = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}