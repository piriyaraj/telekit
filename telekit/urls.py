from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from django.views.decorators.cache import cache_control
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', include('blog.urls')),
    path('admin/', admin.site.urls),
    path('', include('user_profile.urls')),
    path('', include('game.urls')),
    path('superuser/', include('extract.urls')),
    path('robots.txt', include('robots.urls')),
    path('ads.txt', TemplateView.as_view(template_name='text/ads.txt', content_type='text/plain')),

    # Serve static files with cache control
    # path('static/<path:path>', cache_control(max_age=31536000, must_revalidate=True)(serve), {'document_root': settings.STATICFILES_DIRS[0]}),
    path('static/<path:path>', cache_control(no_cache=True, must_revalidate=True)(serve), {'document_root': settings.STATICFILES_DIRS[0]}),
    # max_age is set to 31536000 seconds (1 year)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
