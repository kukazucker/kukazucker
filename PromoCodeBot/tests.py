import unittest
import parse

class TestGetData(unittest.TestCase):
    def test_page(self):    # page upload test                                     
        self.assertIsNone(parse.get_page('https://www.wired.com/coupons/aliexpress'))
    def test_categories(self):  # category getting test
        self.assertTrue(parse.get_categories())
    def test_link(self):    # coverted string test
        self.assertEqual(parse.category_link('Home & Garden'), 'home-garden')
    def test_code(self):    # request a coupon test
        self.assertEqual(parse.get_code('https://www.wired.com/coupons/categories/hobby-lifestyle#id-92176451'), ['Code Sent with E-mail Sign Upo', 'https://www.wired.com/coupons/get/92176451?popup=true'])
    def test_promocodes(self):  # get all promocodes test
        self.assertTrue(parse.get_promocodes('Home & Garden'))

