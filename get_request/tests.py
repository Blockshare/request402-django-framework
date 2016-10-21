"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

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
        resp = self.client.get('/domain_status?uri=google.com')
        self.assertEqual(resp.status_code, 402)
        self.assertEqual(resp.content, b'"Payment Required"')

    def test_domain_ip(self):
        resp = self.client.get('/domain_ip?uri=google.com')
        self.assertEqual(resp.status_code, 402)
        self.assertEqual(resp.content, b'"Payment Required"')

    def test_ip(self):
        resp = self.client.get('/ip')
        self.assertEqual(resp.status_code, 402)
        self.assertEqual(resp.content, b'"Payment Required"')

    def test_get(self):
        resp = self.client.get('/get')
        self.assertEqual(resp.status_code, 402)
        self.assertEqual(resp.content, b'"Payment Required"')

    def test_btc_address(self):
        resp = self.client.get(
            '/bitcoin?address=1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa')
        self.assertEqual(resp.status_code, 402)
        self.assertEqual(resp.content, b'"Payment Required"')

    def test_server_location(self):
        resp = self.client.get('/server-location')
        self.assertEqual(resp.status_code, 402)
        self.assertEqual(resp.content, b'"Payment Required"')

    def test_company_contact(self):
        resp = self.client.get('/company-contact')
        self.assertEqual(resp.status_code, 402)
        self.assertEqual(resp.content, b'"Payment Required"')

    def test_twitter_acct(self):
        resp = self.client.get('/twitter')
        self.assertEqual(resp.status_code, 402)
        self.assertEqual(resp.content, b'"Payment Required"')

    def test_ssl_cert(self):
        resp = self.client.get('/ssl-cert')
        self.assertEqual(resp.status_code, 402)

    def test_ssl_source(self):
        resp = self.client.get('/ssl')
        self.assertEqual(resp.status_code, 402)
        self.assertEqual(resp.content, b'"Payment Required"')

    def test_blacklist(self):
        resp = self.client.get('/blacklist?url=google.com')
        self.assertEqual(resp.status_code, 402)
        self.assertEqual(resp.content, b'"Payment Required"')

    def test_ranking(self):
        resp = self.client.get('/domain_rank?url=google.com')
        self.assertEqual(resp.status_code, 402)
        self.assertEqual(resp.content, b'"Payment Required"')
