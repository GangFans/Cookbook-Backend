from django.http import JsonResponse
from django.test import TestCase, Client
from django.urls import reverse
import json


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_version(self):
        response: JsonResponse = self.client.get(reverse('Book:version'))
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertIn('data', content)
        self.assertEqual(content['data'], 'v0.0.1')
