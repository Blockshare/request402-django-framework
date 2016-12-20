"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.

All of these work with the two1 library to make sure that each endpoint passes.

"""

import mock

from django.test import TestCase

# All of these are simple unittests for each endpoint in the web application.
# Each test passes now but it is alwas good to check to make sure the
# endpoints are still working.


class SimpleTestCase(TestCase):

    def test_index(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_info(self):
        resp = self.client.get('/info')
        self.assertEqual(resp.status_code, 200)

    def test_domain_status(self):
        resp = self.client.get('/domain_status?url=google.com')
        self.assertEqual(resp.status_code, 402)

    @mock.patch('two1.bitserv.django.decorator.Payment.contains_payment',
                 return_value=True)
    def test_domain_buy_status(self, *args):
        resp = self.client.get('/domain_status?url=google.com')
        self.assertEqual(resp.status_code, 200)

    def test_domain_ip(self):
        resp = self.client.get('/domain_ip?uri=google.com')
        self.assertEqual(resp.status_code, 402)

    @mock.patch('two1.bitserv.django.decorator.Payment.contains_payment',
                 return_value=True)
    def test_domain_buy_ip(self, *args):
        resp = self.client.get('/domain_ip?url=google.com')
        self.assertEqual(resp.status_code, 200)

    def test_ip(self):
        resp = self.client.get('/ip')
        self.assertEqual(resp.status_code, 200)

    def test_get(self):
        resp = self.client.get('/get')
        self.assertEqual(resp.status_code, 402)

    @mock.patch('two1.bitserv.django.decorator.Payment.contains_payment',
                 return_value=True)
    def test_buy_get(self, *args):
        resp = self.client.get('/get')
        self.assertEqual(resp.status_code, 200)

    def test_server_location(self):
        resp = self.client.get('/server-location')
        self.assertEqual(resp.status_code, 402)

    @mock.patch('two1.bitserv.django.decorator.Payment.contains_payment',
                 return_value=True)
    def test_buy_server_location(self, *args):
        resp = self.client.get('/server-location')
        self.assertEqual(resp.status_code, 200)

    def test_ssl_cert(self):
        resp = self.client.get('/ssl-cert')
        self.assertEqual(resp.status_code, 402)

    @mock.patch('two1.bitserv.django.decorator.Payment.contains_payment',
                 return_value=True)
    def test_buy_ssl_cert(self, *args):
        resp = self.client.get('/ssl-cert?url=google.com')
        self.assertEqual(resp.status_code, 200)

    def test_ssl_source(self):
        resp = self.client.get('/ssl')
        self.assertEqual(resp.status_code, 402)

    @mock.patch('two1.bitserv.django.decorator.Payment.contains_payment',
                 return_value=True)
    def test_buy_ssl_source(self, *args):
        resp = self.client.get('/ssl?url=google.com')
        self.assertEqual(resp.status_code, 200)

    def test_blacklist(self):
        resp = self.client.get('/blacklist')
        self.assertEqual(resp.status_code, 402)

    @mock.patch('two1.bitserv.django.decorator.Payment.contains_payment',
                 return_value=True)
    def test_buy_blacklist(self, *args):
        resp = self.client.get('/blacklist?url=google.com')
        self.assertEqual(resp.status_code, 200)

    def test_ranking(self):
        resp = self.client.get('/domain_rank?url=google.com')
        self.assertEqual(resp.status_code, 402)

    @mock.patch('two1.bitserv.django.decorator.Payment.contains_payment',
                 return_value=True)
    def test_buy_ranking(self, *args):
        resp = self.client.get('/domain_rank?url=google.com')
        self.assertEqual(resp.status_code, 200)

    def test_search(self):
        resp = self.client.get('/domain_search')
        self.assertEqual(resp.status_code, 402)

    @mock.patch('two1.bitserv.django.decorator.Payment.contains_payment',
                 return_value=True)
    def test_buy_search(self, *args):
        resp = self.client.get('/domain_search?url=google.com')
        self.assertEqual(resp.status_code, 200)

    def test_social(self):
        resp = self.client.get('/domain_social_stats')
        self.assertEqual(resp.status_code, 402)

    @mock.patch('two1.bitserv.django.decorator.Payment.contains_payment',
                 return_value=True)
    def test_buy_social(self, *args):
        resp = self.client.get('/domain_social_stats?url=google.com')
        self.assertEqual(resp.status_code, 200)

    def test_screenshot(self):
        resp = self.client.get('/domain_screenshot')
        self.assertEqual(resp.status_code, 402)

    @mock.patch('two1.bitserv.django.decorator.Payment.contains_payment',
                 return_value=True)
    def test_buy_screenshot(self, *args):
        resp = self.client.get('/domain_screenshot?url=google.com')
        self.assertEqual(resp.status_code, 200)
