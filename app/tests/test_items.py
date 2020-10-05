import unittest
import json

from app import db
from app.tests.base import BaseTestCase
from app.models import User, ExpiredToken


def register_user(self, full_names, email, password):
    return self.client.post(
        '/auth/register',
        data=json.dumps(dict(
            full_names=full_names,
            email=email,
            password=password
        )),
        content_type='application/json',
    )


class TestItemBlueprint(BaseTestCase):
    def test_add_image(self):
        """ Test for image addition """
        with self.client:
            response = self.client.post(
                '/items/add',
                data=json.dumps(dict(
                    item='item1.png',
                    item_name='item_name',
                    item_description='Sample'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Item added successfully.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_add_existing_image(self):
        """ Test for image addition """
        with self.client:
            response = self.client.post(
                '/items/add',
                data=json.dumps(dict(
                    item='item1.png',
                    item_name='item_name',
                    item_description='Sample'
                )),
                content_type='application/json'
            )
            response1 = self.client.post(
                '/items/add',
                data=json.dumps(dict(
                    item='item1.png',
                    item_name='item_name',
                    item_description='Sample'
                )),
                content_type='application/json'
            )
            data = json.loads(response1.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Item with the same name already exists.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)


