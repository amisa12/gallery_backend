# project/server/tests/test_config.py


import unittest

from flask import current_app
from flask_testing import TestCase

from app import app


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('app.config.DevelopmentConfig')
        return app


    class TestTestingConfig(TestCase):
        def create_app(self):
            app.config.from_object('app.config.TestingConfig')
            return app

        def test_app_is_testing(self):
            self.assertFalse(app.config['SECRET_KEY'] is 'my_precious')
            self.assertTrue(app.config['DEBUG'])
            self.assertTrue(
                app.config['SQLALCHEMY_DATABASE_URI'] == 'postgresql://postgres:@localhost/lending_v2_test'
            )

class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('app.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        self.assertTrue(app.config['DEBUG'] is False)


if __name__ == '__main__':
    unittest.main()
