# -*- coding: utf-8 -*-
from django.shortcuts import redirect
#from django.template import RequestContext

def my404view(request):
    return redirect('/')

