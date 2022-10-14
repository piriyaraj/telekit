from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='superuser'),
    path('extract/',views.extract,name='extract')
]   