"""pztsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, re_path
from django.views.generic.base import RedirectView
from . import views


urlpatterns = [
    
    #http://127.0.0.1:8000/plotter/  
    path('', views.index, name='index'),   
    


    #http://127.0.0.1:8000/plotter/compare/numeric
    #re_path(r'^compare/(?P<int:count>[0-9]{1})', views.html_compare, name='html_compare'),    
    re_path(r'^compare/(?P<count>\d+)', views.html_compare, name='html_compare'), 
  
    #http://127.0.0.1:8000/plotter/compare/list_of_elements
    re_path(r'^compare/(?P<estr>.*)', views.b64_compare, name='b64_compare'),   
    

]
    #This URL pattern is redundant; same as compare/1
    #http://127.0.0.1:8000/plotter/select
    #path('select', views.select, name='select'),

    #These patterns are no longer necessary (I think?)
    #http://127.0.0.1:8000/plotter/XX1234
    #re_path(r'(?P<sn>[a-zA-Z]{2}[0-9]{4}?)/$', views.plot, name='plot'), 
    
    #http://127.0.0.1:8000/plotter/XX1234/L/4/absplot
    #re_path(r'^(?P<sn>[a-zA-Z]{2}[0-9]{4})/(?P<bt>[LH]{1})/(?P<eln>[0-9]{1})/(?P<ptype>.*)', views.html_image, name='html_image'),  
    
    #http://127.0.0.1:8000/plotter/image/XX1234/L/4/absplot
    #re_path(r'^image/(?P<sn>[a-zA-Z]{2}[0-9]{4})/(?P<bt>[LH]{1})/(?P<eln>[0-9]{1})/(?P<ptype>.*)', views.b64_image, name='b64_image'),