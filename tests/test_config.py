# tests/test_config.py


import unittest

from flask import Flask
from flask import current_app
from flask_testing import TestCase
from config import app_config
from app import create_app



class TestDevelopmentConfig(TestCase):    

    def create_app(self):
        app = create_app('development')
        return app

    def test_app_is_development(self):
        app = create_app('development')
        self.assertFalse(app.config['SECRET_KEY'] is 'my_precious')
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == 'postgresql://Santuri:Sifumbukh0@localhost/brighteventsapi'
        )


class TestTestingConfig(TestCase):
    def create_app(self):
        app = create_app('testing')
        return app

    def test_app_is_testing(self):
        app = create_app('testing')
        self.assertFalse(app.config['SECRET_KEY'] is 'my_precious')
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == 'postgresql://Santuri:Sifumbukh0@localhost/brighteventsapi_test'
        )


class TestProductionConfig(TestCase):
    def create_app(self):
        app = create_app('production')
        app.config.from_object(app_config['production'])
        return app

    def test_app_is_production(self):
        app = create_app('production')
        self.assertTrue(app.config['DEBUG'] is False)


if __name__ == '__main__':
    unittest.main()
