from django.urls import path
from game import views

urlpatterns = [
    path('spin-earn-points',views.spinner,name='spin-earn-points'),
    path('spin-handler/<str:points>',views.spinHandler,name='spin-handler')
]