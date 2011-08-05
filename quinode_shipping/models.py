# -*- coding: utf-8 -*-

"""
"""

from django.db import models, IntegrityError
from colissimo.models import Region
from decimal import Decimal
import types
from django.utils.translation import ugettext_lazy as _

class LetterRate(models.Model):
    # Up to this weight (in kg)
    weight = models.DecimalField(_(u'Weight'), max_digits=5, decimal_places=2)
    # Rate in Euro
    price = models.DecimalField(_(u'Price'), max_digits=5, decimal_places=2)
    regions = models.ManyToManyField(Region, verbose_name=_(u'Region'))
    securexport = models.DecimalField(_(u'SecurExport'), max_digits=5, decimal_places=2, default='0.0')
    
    class Meta:
        verbose_name = _('Letter rate')
        verbose_name_plural = _('Letter rates')
    
    @staticmethod
    def get_rates(country, weight):
        """
        Example: lowest rate for a 4.2 kg box to France:
                 Rate.get_rates('France', 4.2).get(recommanded__level='R0')
        """
        if type(country) != types.StringType and type(country) != types.UnicodeType:
            raise TypeError, _(u"Country must be a string, not %s") % type(country)
        if type(weight) != types.FloatType and type(weight) != types.IntType:
            raise TypeError, _("Weight must be a float")
        r = Region.get_region_from_country(country)
        if r is None:
            raise ValueError, _(u"Bad country value '%s': could not determine region") % country
        rates = LetterRate.objects.filter(weight__gte=Decimal(str(weight)), regions=r).order_by('weight')
        if rates.count()==0:
            raise LetterRate.DoesNotExist
        w = rates[0].weight
        return LetterRate.objects.get(weight=w, regions=r)
            
        
    def get_total_price(self):
        return self.price + self.securexport

    def __unicode__(self):
        return _(u"LetterRate: max %.2fkg (%s)") % (self.weight, u','.join([unicode(x) for x in self.regions.all()]))

from product.models import Product

SATCHMO_PRODUCT=True

def get_product_types():
    """
    Returns a tuple of all product subtypes this app adds
    """
    return ('Shipping', )

class Shipping(models.Model):
    product = models.OneToOneField(Product, verbose_name=_('Product'), primary_key=True)
    is_bulky = models.BooleanField(verbose_name=_('Is bulky?'), default=True)

    def _get_subtype(self):
        """
        Has to return the name of the product subtype
        """
        return 'Shipping'

    def __unicode__(self):
        return self.product.name

    class Meta:
        verbose_name = _('Product shipping')
        verbose_name_plural = _('Products shipping')