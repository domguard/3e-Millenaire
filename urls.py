from django.conf.urls.defaults import *

handler404 = 'localsite.views.my404view'



from satchmo_store.urls import urlpatterns

#from localsite.urls import *

urlpatterns += patterns('',
    url(r'^admin_tools/', include('admin_tools.urls')),
)