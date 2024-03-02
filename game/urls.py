from django.urls import path
from game import views

urlpatterns = [
    path('spin-earn-points',views.spinner,name='spin-earn-points'),
    path('spin-handler/<str:points>',views.spinHandler,name='spin-handler'),
    path('claim-bonus',views.claim_bonus,name='claim-bonus'),
    path('ref/telekit<str:referral_code>',views.referral_handler,name='referral-handler'),
    path('referral',views.referral,name='referral'),
]