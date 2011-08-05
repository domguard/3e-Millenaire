# -*- coding: utf-8 -*-

"""
Colissimo shipping : Calculate the shipping fees based on colissimo prices
Depends of the django_colissimo app
"""

# Note, make sure you use decimal math everywhere!
from decimal import Decimal
from django.utils.translation import ugettext as _
from shipping.modules.base import BaseShipper
from colissimo.models import Rate
from livesettings import config_get_group, config_value
from models import LetterRate

class Shipper(BaseShipper):

    id = "Quinode"
    
    def __init__(self, cart=None, contact=None, service_type=None):

        self.cart = cart
        self.contact = contact
        self._rate = None
        self._rate_calculated = False
        self.settings = config_get_group('quinode_shipping')
        
    def __str__(self):
        """
        This is mainly helpful for debugging purposes
        """
        return "Quinode"
    
    def __unicode__(self):
        return u"Quinode"
        
    def description(self):
        """
        A basic description that will be displayed to the user when selecting their shipping options
        """
        rate = self._calculate_rate()
        if type(rate) == LetterRate:
            desc = _(u'{0} Kg').format(rate.weight)
            if rate.securexport > Decimal('0'):
                desc += u' + {0}€ Securexport'.format(rate.securexport)
            return desc
        return _(u'{0} Kg - {1}').format(rate.weight, rate.region.name)
        
    def _is_product_bulky(self, product):
        """returns True if bulky flag is raised for this product"""
        if hasattr(product, 'shipping') and product.shipping:
            return product.shipping.is_bulky
        return False
    
    def _get_product_weight(self, product):
        """returns the weight of the product or default weight if not set"""
        if product.weight_units and product.weight!=None and product.weight_units.lower() == 'kg':
            return product.weight
        
        #Infos de poids du produit non défini: lit la valeur par défaut depuis la config
        try:
            default_product_weigth = Decimal(unicode(self.settings.DEFAULT_PRODUCT_WEIGHT))
        except TypeError, err:
            default_product_weigth = Decimal('0')
        return default_product_weigth

    def _calculate_rate(self):
        if self._rate_calculated:
            return self._rate
        self._rate = self._do_calculate_rate()
        self._rate_calculated = True
        return self._rate

    def _do_calculate_rate(self):
        #Calcul du poids et encombrement du colis
        total_weight = Decimal('0')
        has_bulky_product = False
        for cart_item in self.cart.cartitem_set.all(): #Pour chaque article du panier
            
            #Verifie que le colis ne contient pas de produit encombrant
            has_bulky_product = has_bulky_product or self._is_product_bulky(cart_item.product)
            
            #Poids du produit
            product_weight = self._get_product_weight(cart_item.product)
                
            #MAJ le poids du colis
            total_weight += product_weight * cart_item.quantity
        
        #Recupere le pays d'expedition
        country = self.contact.shipping_address.country.name
        
        #si le panier contient un produit encombrant : on ne teste pas l'envoi en lettre suivie
        if not has_bulky_product:
            try:
                #Recherche d'un tarif lettre suivie pour le poids du colis et pays d'expedition
                rate = LetterRate.get_rates(country, float(total_weight))
                #Colis expediable en lettre suivie: retourne le prix
                return rate  #Type LetterRate
            except (LetterRate.DoesNotExist, ValueError):
                pass #Colis non expediable en lettre suivie: continue et test le colissimo
        
        #Recherche d'un tarif colissimo pour le poids du colis, pays d'expedition et niveau de recommandé configuré
        #Le niveau de recommandé est lue depuis la configuration livesettings
        try:
            recommanded_level = self.settings.RECOMMANDED_LEVEL
            rate = Rate.get_rates(country, float(total_weight)).get(recommanded__level=recommanded_level) #Type Rate
        except Rate.DoesNotExist, msg:
            #Pas de tarif correspondant : essai avec un niveau de recommandé minimal
            try:
                rate = Rate.get_rates(country, float(total_weight)).get(recommanded__level='R0') #Type Rate
            except Rate.DoesNotExist, msg:
                #Pas de tarif : Envoi impossible
                rate = None
        except ValueError:
            rate = None
        
        #return the price
        return rate

    def cost(self):
        rate = self._calculate_rate()
        if type(rate) == LetterRate:
            return rate.get_total_price()
        return rate.price

    def method(self):
        """
        Describes the actual delivery service (Mail, FedEx, DHL, UPS, etc)
        """
        rate = self._calculate_rate()
        if type(rate) == LetterRate:
            return _(u'Lettre suivie')
        return _(u"Colissimo")

    def expectedDelivery(self):
        """
        Can be a plain string or complex calcuation returning an actual date
        """
        if self.contact.shipping_address.country.name == 'France':
            return _(u"2 business days") #France
        return _(u"4 to 8 business days") #International

    def valid(self, order=None):
        """
        Can do complex validation about whether or not this option is valid.
        For example, may check to see if the recipient is in an allowed country
        or location.
        """
        rate = self._calculate_rate()
        return (rate != None)

