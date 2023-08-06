from ds4biz_commons.utils.requests_utils import URLRequest
from unittest.case import TestCase

class URLRequestTest(TestCase):

    def test_simple(self):
        u=URLRequest("http://example.com")
        self.assertEqual(u.fragment.get_base(),u['fragment'].get_base())