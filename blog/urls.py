from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('loadmore/', views.loadmore, name='loadmore'),
    path('doc/<str:path>',views.docfiles,name='docs'),
    path('group/find',views.find,name='find'),
    path('group/<str:path>',views.groupfiles,name='groups'),
    path('join/<str:path>',views.links,name='links'),
    path('category/<str:path>',views.category,name='category'),
    path('country/<str:path>',views.country,name='country'),
    path('language/<str:path>',views.language,name='language'),
    path('tag/<str:path>',views.tag,name='language'),
    path('search/',views.search,name='search'),
    path('addgroup',views.addgroup,name='search'),
]   