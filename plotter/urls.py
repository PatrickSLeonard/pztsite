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
    re_path(r'^compare/(?P<count>[1-9]+[0-9]*)', views.html_compare, name='html_compare'), 
    
    #http://127.0.0.1:8000/plotter/compare/<ANYTHING ELSE>
    re_path(r'^compare/.*', views.html_redir, name='html_redir'), 

    #http://127.0.0.1:8000/plotter/html/list_of_elements
    re_path(r'^html/(?P<estr>.*)', views.testview, name='testview'),
    
    #http://127.0.0.1:8000/plotter/image/list_of_elements
    re_path(r'^image/(?P<estr>.*)', views.imageview, name='imageview'),    
    
]

# Note: if I cared what the extra bits were I oan use:
#   re_path(r'^compare/(.*)', views.html_redir, name='html_redir'), 