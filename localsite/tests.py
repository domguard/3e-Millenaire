# -*- coding: utf-8 -*-

from django.test import TestCase

from validations import is_ean

class EanValidationTest(TestCase):
    
    def _call_validation(self, value):
        is_ok, ret_value = is_ean(value)
        self.assertEquals(value, ret_value)
        return is_ok
    
    def test_ean_not_a_number(self):
        is_ok = self._call_validation('a'*13)
        self.assertFalse(is_ok)
        
    def test_ean_too_short(self):
        is_ok = self._call_validation('1'*12)
        self.assertFalse(is_ok)
        
    def test_ean_too_long(self):
        is_ok = self._call_validation('1'*14)
        self.assertFalse(is_ok)
        
    def test_ean_empty(self):
        is_ok = self._call_validation('')
        self.assertFalse(is_ok)
        
    def test_ean_ok(self):
        is_ok = self._call_validation('1'*13)
        self.assertTrue(is_ok)
        