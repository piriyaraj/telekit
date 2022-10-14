from django.urls import path
from . import views
from blog.sitemap import countrySitemap, categorySitemap, languageSitemap, linkSitemap, StaticViewSitemap
from django.contrib.sitemaps.views import sitemap


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
    path('tag/<str:path>',views.tag,name='tag'),
    path('search/',views.search,name='search'),
    path('addgroup',views.addgroup,name='search'),
]   

sitemapUrls=[
    path("country-sitemap.xml", sitemap, {'sitemaps': {"blog": countrySitemap}}),
    path("category-sitemap.xml", sitemap, {'sitemaps': {"blog": categorySitemap}}),
    path("language-sitemap.xml", sitemap, {'sitemaps': {"blog": languageSitemap}}),
    path("link-sitemap.xml", sitemap, {'sitemaps': {"blog": linkSitemap}}),
    path("static-sitemap.xml", sitemap, {'sitemaps': {"blog": StaticViewSitemap}}),
]

urlpatterns+=sitemapUrls