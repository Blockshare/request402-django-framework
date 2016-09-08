"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


class SimpleTestCase(TestCase):
    def test_info(self):
        resp = self.client.get('/info')
        self.assertEqual(resp.status_code, 200)

    def test_get_status(self):
        resp = self.client.get('/get_status?uri=google.com')
        self.assertEqual(resp.status_code, 402)

    def test_get_ip(self):
        resp = self.client.get('/get_ip?uri=google.com')
        self.assertEqual(resp.status_code, 402)

    def test_ip(self):
        resp = self.client.get('/ip')
        self.assertEqual(resp.status_code, 402)

    def test_btc_address(self):
        resp = self.client.get('/bitcoin?address=1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa')
        self.assertEqual(resp.status_code, 402)

    def test_ipinfo(self):
        resp = self.client.get('/ipinfo')
        self.assertEqual(resp.status_code, 402)
