from django.conf.urls.defaults import *
#from satchmo_utils.urlhelper import replace_urlpattern
#from product.urls import products

#urlpatterns = patterns('',
#    (r'example/', 'simple.localsite.views.example', {}),
#)

#replacement = url(r'^(?P<parent_slugs>([-\w]+/)*)?(?P<slug>[-\w]+)/$',
#                  'pasma.custom_satchmo_views.category_view', {}, 'satchmo_category')
#replace_urlpattern(urlpatterns, replacement)

#urlpatterns = patterns('',
#    url(r'^/(?P<category_slug>[-\w]+)/(?P<product_slug>[-\w]+)/$', 'get_product', {}, 'satchmo_product_and_cat'),
#)    

#for r in replacements:
#    replace_urlpattern(products.urlpatterns, r)
#

#from products.models import Product
#
#def get_product_and_cat_absolute_url(product):
#    return urlresolvers.reverse('satchmo_product_and_cat',
#        kwargs={'product_slug': product.slug, 'category_slug': 'toto'})
#
#Product.get_absolute_url = get_product_and_cat_absolute_url
#
#    
