from django.conf.urls.defaults import *

from satchmo_store.urls import urlpatterns

#from localsite.urls import *

urlpatterns += patterns('',
    url(r'^admin_tools/', include('admin_tools.urls')),
)