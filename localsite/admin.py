# -*- coding: utf-8 -*-

from django.contrib import admin

from product.models import Product, Category
from django import forms
from product.admin import ProductOptions
from django.utils.translation import ugettext_lazy as _

from django.contrib.admin.widgets import FilteredSelectMultiple

class SortedQueryset:
    def __init__(self, qs):
        self.qs = qs
        
    def all(self):
        #Permet de trier les catégories par le chemin complet (parents inclus)
        items = list(self.qs.all())
        def sort_by_unicode(x): return unicode(x)
        items.sort(key=sort_by_unicode)
        for i in items:
            yield i

    def __getattr__(self, name):
        #Pour toutes les autres méthodes que all : appelle la méthode du queryset
        return getattr(self.qs, name)

from django.db import models
from tinymce.widgets import AdminTinyMCE

import locale
locale.setlocale( locale.LC_ALL, 'fr_FR.UTF-8' )
def prix_lisible(obj):
    return locale.currency(obj.unit_price,grouping=True)
prix_lisible.short_description = 'prix'

def cat_principale(obj):
    return obj.category.all()[0]
cat_principale.short_description = 'Catégorie'


class ProductAdminForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(
        queryset=SortedQueryset(Category.objects),
        widget=FilteredSelectMultiple('category', False)
    )
    description = forms.CharField(widget=AdminTinyMCE(attrs={'cols':80,'rows':20}))
    class Meta:
        model = Product


class ProductAdmin(ProductOptions):
    form = ProductAdminForm
    list_display = ('name','active','featured', prix_lisible,cat_principale)
    list_display_links = ('name',)
    list_filter = ('date_added','active','featured')
    list_editable = ('active','featured')
    fieldsets = (
            (None, {'fields': ('site','category', 'name', 'description', 'short_description','active', 'featured','ordering', 'shipclass')}), 
            (_('Meta Data'), {'fields': ('meta',), 'classes': ('collapse',)}),
            (_('Item Dimensions'), {'fields': (('length', 'length_units','width','width_units','height','height_units'),('weight','weight_units'))}),
            (_('Tax'), {'fields':('taxable', 'taxClass'), 'classes': ('collapse',)}),
            (_('Related Products'), {'fields':('related_items',)}), 
            )
    filter_horizontal = ('related_items','also_purchased')
            

admin.site.unregister(Product)
admin.site.register(Product, ProductAdmin)