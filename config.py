import os
database_name = 'brighteventsapi'
test_db = 'brighteventsapi_test'
postgres_local_base = 'postgresql://Santuri:Sifumbukh0@localhost/'


class Config(object):
    """ Parent configuration class."""
    DEBUG = False

class DevelopmentConfig(Config):
    """ Configurations for Development."""
    DEBUG = True
    SECRET_KEY = "tonystarktheironman"
    SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name

class TestingConfig(Config):
    """ Configurations for Testing, with a separate test database."""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = postgres_local_base + test_db

class StagingConfig(Config):
    """ Configurations for Staging."""
    DEBUG = True

class ProductionConfig(Config):
    """ Configurations for Production."""
    SECRET_KEY="MarvelAgentsOfShield" 	
    DEBUG = False
    TESTING = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}