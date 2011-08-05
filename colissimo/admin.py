# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from colissimo.models import Recommanded, Region, Rate
    
admin.site.register(Region)
admin.site.register(Rate)
admin.site.register(Recommanded)
