from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='superuser'),
    path('extract/',views.extract,name='extract'),
    path('makepage/',views.makeHtml,name='makeHtml'),
    path('removeinvalidurl/',views.removeInvalidurl,name='removeinvalidurl')
]   