# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from models import LetterRate, Shipping
from django import forms
from django.core.exceptions import ValidationError
    
class LetterRateAdminForm(forms.ModelForm):

    class Meta:
        model = LetterRate
        
    def clean_regions(self):
        id = self.initial.get('id')
        duplicated_region = ''
        weight = self.cleaned_data['weight']
        for region in self.cleaned_data['regions']:
            qs = self.Meta.model.objects.filter(regions=region, weight=weight)
            if id:
                qs = qs.exclude(id=id)
            if qs.count():
                raise ValidationError('A letter rate already exist for (weight={0}, region={1})'.format(weight, region))
        return self.cleaned_data['regions']
 
    
class LetterRateAdmin(admin.ModelAdmin):
    form = LetterRateAdminForm
    
    list_display = ('weight', '_regions', 'price', 'securexport')
    list_editable = ('price', 'securexport')
    
    def _regions(self, instance):
        return u', '.join(x.name for x in instance.regions.all())
    _regions.short_description = u'Regions'
    
    ordering = ('weight',)
    
admin.site.register(LetterRate, LetterRateAdmin)

class ShippingAdmin(admin.ModelAdmin):
    list_display = ('product', 'is_bulky')
    list_editable = ('is_bulky',)
    
admin.site.register(Shipping, ShippingAdmin)