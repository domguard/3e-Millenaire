# -*- coding: utf-8 -*-

from django.contrib import admin

from product.models import Product, Category
from django import forms
from product.admin import ProductOptions

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


class ProductAdminForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(
        queryset=SortedQueryset(Category.objects),
        widget=FilteredSelectMultiple('category', False)
    )
    class Meta:
        model = Product

from tinymce.widgets import AdminTinyMCE

class ProductAdmin(ProductOptions):
    form = ProductAdminForm
    formfield_overrides = {
        models.TextField: {'widget': AdminTinyMCE},
        }
        
admin.site.unregister(Product)
admin.site.register(Product, ProductAdmin)