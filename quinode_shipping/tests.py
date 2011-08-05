# -*- coding: utf-8 -*-

from django.test import TestCase

from model_mommy import mommy

from l10n.models import Country
from decimal import Decimal
from django.contrib.sites.models import Site
from django.utils.translation import ugettext as _

from satchmo_store.contact.models import AddressBook, Contact
from satchmo_store.shop.models import Cart, CartItem
from product.models import Discount, Product, Price

from shipper import Shipper
from config import define_default_product_weight, define_recommanded_level
from models import Shipping

class QuinodeShippingTest(TestCase):
    fixtures = ['letter_rates.json']
    
    def setUp(self):
        define_recommanded_level('R0')
        define_default_product_weight('0.05')
    
    def _create_cart(self, weights_quantity, country_name=u'France'):
        country = mommy.make_one(Country, name=country_name)
        contact = mommy.make_one(Contact)
        shipping_adrress = mommy.make_one(AddressBook, contact=contact, country=country, is_default_shipping=True)
        cart = mommy.make_one(Cart, site=Site.objects.get_current(), customer=contact)
        for args in weights_quantity:
            if len(args) == 3:
                args = args + (None,) #by default : bulky is False
            weight, unit, quantity, bulky = args
            
            kwargs = {}
            if weight!=None: kwargs['weight']= weight
            if unit!=None: kwargs['weight_units']= unit
            product = mommy.make_one(Product, **kwargs)
            if bulky != None:
                shipping = mommy.make_one(Shipping, product=product, is_bulky=bulky)
            
            price = mommy.make_one(Price, product=product, price='1.0')
            cart_item = mommy.make_one(CartItem, product=product, quantity=quantity, cart=cart)
        return Shipper(cart=cart, contact=contact)
        
    def _assertIsColissimo(self, shipper, is_colissimo):
        self.assertEquals(is_colissimo, bool(shipper.method().find(_(u'Colissimo'))>=0))
        
    def test_calculate_letter(self):
        shipper = self._create_cart([('0.49', 'kg', 1)])
        self.assertEqual(shipper.cost(), Decimal('4.9'))
        self._assertIsColissimo(shipper, False)
        self.assertEqual(shipper.description(), u'0.5 Kg')
        
    def test_calculate_letter_limit(self):
        shipper = self._create_cart([('0.5', 'kg', 1)])
        self.assertEqual(shipper.cost(), Decimal('4.9'))
        self._assertIsColissimo(shipper, False)
        self.assertEqual(shipper.description(), u'0.5 Kg')

    def test_calculate_colissimo(self):
        shipper = self._create_cart([('0.51', 'kg', 1)])
        self.assertEqual(shipper.cost(), Decimal('6.95'))
        self._assertIsColissimo(shipper, True)
        self.assertEqual(shipper.description(), u'1 Kg - France - Monaco - Andore')
                
    def test_calculate_10kg_shipping(self):
        shipper = self._create_cart([('10', 'kg', 1)])
        self.assertEqual(shipper.cost(), Decimal('15.95'))
        self._assertIsColissimo(shipper, True)
        self.assertEqual(shipper.description(), u'10 Kg - France - Monaco - Andore')
        
    def test_calculate_R1_letter(self):
        define_recommanded_level('R1') #No impact: this setting is only for colissimo
        shipper = self._create_cart([('0.5', 'kg', 1)])
        self.assertEqual(shipper.cost(), Decimal('4.9'))
        self._assertIsColissimo(shipper, False)
        self.assertEqual(shipper.description(), u'0.5 Kg')
        
    def test_calculate_R1_colissimo(self):
        define_recommanded_level('R1')
        shipper = self._create_cart([('0.51', 'kg', 1)])
        self.assertEqual(shipper.cost(), Decimal('9.45'))
        self._assertIsColissimo(shipper, True)
        self.assertEqual(shipper.description(), u'1 Kg - France - Monaco - Andore')
        
    def test_calculate_invalid_recommanded_level(self):
        define_recommanded_level('???')
        shipper = self._create_cart([('0.51', 'kg', 1)])
        self.assertEqual(shipper.cost(), Decimal('6.95')) #By default R0
        self._assertIsColissimo(shipper, True)
        self.assertEqual(shipper.description(), u'1 Kg - France - Monaco - Andore')
        
    def test_calculate_R4_5kg(self):
        define_recommanded_level('R1')
        shipper = self._create_cart([('5', 'kg', 1)])
        self.assertEqual(shipper.cost(), Decimal('13.45'))
        self._assertIsColissimo(shipper, True)
        self.assertEqual(shipper.description(), u'5 Kg - France - Monaco - Andore')
        
    def test_calculate_product_quantity(self):
        shipper = self._create_cart([('0.1', 'Kg', 9)])
        self.assertEqual(shipper.cost(), Decimal('6.95'))
        self._assertIsColissimo(shipper, True)
        self.assertEqual(shipper.description(), u'1 Kg - France - Monaco - Andore')
        
    def test_calculate_several_products(self):
        shipper = self._create_cart([('0.1', 'kg', 1), ('0.2', 'kg', 2), ('0.45', 'kg', 1)])
        self.assertEqual(shipper.cost(), Decimal('6.95'))
        self._assertIsColissimo(shipper, True)
        self.assertEqual(shipper.description(), u'1 Kg - France - Monaco - Andore')
        
    def test_calculate_letter_zone_a(self):
        shipper = self._create_cart([('0.1', 'kg', 1)], u'Italy')
        self.assertEqual(shipper.cost(), Decimal('4.8'))
        self._assertIsColissimo(shipper, False)
        self.assertEqual(shipper.description(), u'0.1 Kg + 3€ Securexport')
        
    def test_calculate_colissimo_zone_a(self):
        shipper = self._create_cart([('0.51', 'kg', 1)], u'Italy')
        self.assertEqual(shipper.cost(), Decimal('16.15'))
        self._assertIsColissimo(shipper, True)
        self.assertEqual(shipper.description(), u'1 Kg - International Zone A')
        
    def test_calculate_letter_zone_b(self):
        shipper = self._create_cart([('0.1', 'kg', 1)], u'Algeria')
        self.assertEqual(shipper.cost(), Decimal('5.35'))
        self._assertIsColissimo(shipper, False)
        self.assertEqual(shipper.description(), u'0.1 Kg + 3€ Securexport')
        
    def test_calculate_colissimo_zone_b(self):
        shipper = self._create_cart([('0.51', 'kg', 1)], u'Algeria')
        self.assertEqual(shipper.cost(), Decimal('19.8'))
        self._assertIsColissimo(shipper, True)
        self.assertEqual(shipper.description(), u'1 Kg - International Zone B')
        
    def test_calculate_letter_zone_c(self):
        shipper = self._create_cart([('0.1', 'kg', 1)], u'Benin')
        self.assertEqual(shipper.cost(), Decimal('5.35'))
        self._assertIsColissimo(shipper, False)
        self.assertEqual(shipper.description(), u'0.1 Kg + 3€ Securexport')

    def test_calculate_colissimo_zone_c(self):
        shipper = self._create_cart([('0.51', 'kg', 1)], u'Benin')
        self.assertEqual(shipper.cost(), Decimal('23.20'))
        self._assertIsColissimo(shipper, True)
        self.assertEqual(shipper.description(), u'1 Kg - International Zone C')
        
    def test_calculate_letter_zone_d(self):
        shipper = self._create_cart([('0.09', 'kg', 1)], u'Japan')
        self.assertEqual(shipper.cost(), Decimal('5.35'))
        self._assertIsColissimo(shipper, False)
        self.assertEqual(shipper.description(), u'0.1 Kg + 3€ Securexport')

    def test_calculate_colissimo_zone_d(self):
        shipper = self._create_cart([('0.51', 'kg', 1)], u'Japan')
        self.assertEqual(shipper.cost(), Decimal('26.40'))
        self._assertIsColissimo(shipper, True)
        self.assertEqual(shipper.description(), u'1 Kg - International Zone D')
        
    def test_calculate_letter_tom(self):
        shipper = self._create_cart([('0.1', 'kg', 1)], u'Guadeloupe')
        self.assertEqual(shipper.cost(), Decimal('5.35'))
        self._assertIsColissimo(shipper, False)
        self.assertEqual(shipper.description(), u'0.1 Kg + 3€ Securexport')
        
    def test_calculate_colissimo_tom(self):
        shipper = self._create_cart([('0.51', 'kg', 1)], u'Guadeloupe')
        self.assertEqual(shipper.cost(), Decimal('12.7'))
        self._assertIsColissimo(shipper, True)
        self.assertEqual(shipper.description(), u'1 Kg - Outre-mer OM1')
    
    def test_calculate_letter_utf(self):
        shipper = self._create_cart([('0.1', 'kg', 1)], u'Réunion')
        self.assertEqual(shipper.cost(), Decimal('5.35'))
        self._assertIsColissimo(shipper, False)
        self.assertEqual(shipper.description(), u'0.1 Kg + 3€ Securexport')
        
    def test_calculate_colissimo_utf(self):
        shipper = self._create_cart([('0.51', 'kg', 1)], u'Réunion')
        self.assertEqual(shipper.cost(), Decimal('12.7'))
        self._assertIsColissimo(shipper, True)
        self.assertEqual(shipper.description(), u'1 Kg - Outre-mer OM1')
        
    def test_calculate_wrong_weight_unit(self):
        #wrong units are not taken into account
        define_default_product_weight('0.3')
        shipper = self._create_cart([('0.3', 'kg', 1), ('0.1', 'lb', 1)])
        self.assertEqual(shipper.cost(), Decimal('6.95'))
        self._assertIsColissimo(shipper, True)
        self.assertEqual(shipper.description(), u'1 Kg - France - Monaco - Andore')
        
    def test_calculate_no_weight(self):
        #wrong units are not taken into account
        define_default_product_weight('1')
        #None Kg --> 0 Kg
        shipper = self._create_cart([('0.6', 'kg', 1), (None, '', 1), (None, 'kg', 1), (0, 'kg', 1)])
        self.assertEqual(shipper.cost(), Decimal('8.95'))
        self._assertIsColissimo(shipper, True)
        self.assertEqual(shipper.description(), u'3 Kg - France - Monaco - Andore')
        
    def test_calculate_letter_no_weight(self):
        #wrong units are not taken into account
        define_default_product_weight('0.05')
        shipper = self._create_cart([('0.15', 'kg', 1), (None, '', 1), (None, 'kg', 1), (0, 'kg', 1)])
        self.assertEqual(shipper.cost(), Decimal('3.65'))
        self._assertIsColissimo(shipper, False)
        self.assertEqual(shipper.description(), u'0.25 Kg')
        
    def test_calculate_letter_bulky_product(self):
        shipper = self._create_cart([('0.05', 'kg', 1), ('0.1', 'kg', 2, False), ('0.1', 'kg', 1, True)])
        self.assertEqual(shipper.cost(), Decimal('5.6'))
        self._assertIsColissimo(shipper, True)
        self.assertEqual(shipper.description(), u'0.5 Kg - France - Monaco - Andore')
        
    def test_calculate_letter_no_bulky_product(self):
        shipper = self._create_cart([('0.05', 'kg', 1), ('0.1', 'kg', 2, False)])
        self.assertEqual(shipper.cost(), Decimal('3.65'))
        self._assertIsColissimo(shipper, False)
        self.assertEqual(shipper.description(), u'0.25 Kg')
        
    def test_calculate_collisimo_bulky_product(self):
        shipper = self._create_cart([('0.5', 'kg', 1), ('0.1', 'kg', 2), ('0.1', 'kg', 1, True)])
        self.assertEqual(shipper.cost(), Decimal('6.95'))
        self._assertIsColissimo(shipper, True)
        self.assertEqual(shipper.description(), u'1 Kg - France - Monaco - Andore')
        
    def test_calculate_overweight(self):
        shipper = self._create_cart([('30', 'kg', 1), ('1', 'kg', 1)])
        self.assertFalse(shipper.valid())
        
    def test_calculate_letter_unknown_country(self):
        shipper = self._create_cart([('0.1', 'kg', 1)], u'Utopia')
        self.assertFalse(shipper.valid())
        
    def test_calculate_colissimo_unknown_country(self):
        shipper = self._create_cart([('0.51', 'kg', 1)], u'Utopia')
        self.assertFalse(shipper.valid())

