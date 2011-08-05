# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from livesettings import *

SHIP_MODULES = config_get('SHIPPING', 'MODULES')

SHIP_MODULES.add_choice(('quinode_shipping', 'Quinode'))

SHIPPING_GROUP = ConfigurationGroup('quinode_shipping',
    _(u"Quinode shipping moudule parameters"), requires = SHIP_MODULES)

def define_recommanded_level(default_level):
    config_register_list(
        StringValue(SHIPPING_GROUP,
            'RECOMMANDED_LEVEL',
            description=_("Colissimo Insurance level"),
            default=default_level
        )
    )
define_recommanded_level('R0')
    
def define_default_product_weight(default_weight):
    config_register_list(
        StringValue(SHIPPING_GROUP,
            'DEFAULT_PRODUCT_WEIGHT',
            description=_("Default product weight"),
            default=default_weight
        )
    )
define_default_product_weight('0.05')
        
