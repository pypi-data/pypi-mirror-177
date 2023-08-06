"""URL patterns of the collectivo core."""
from django.urls import path, re_path, include
from django.conf import settings
from django.contrib.staticfiles.views import serve
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from collectivo import views


app_name = 'collectivo'

urlpatterns = [
    # Core API views
    path('api/collectivo/v1/version/',
         views.VersionView.as_view(), name='version'),

    # API Documentation
    path('api/collectivo/v1/schema/',
         SpectacularAPIView.as_view(), name='api-schema'),
    path('api/docs/',
         SpectacularSwaggerView.as_view(url_name='collectivo:api-schema'),
         name='api-docs'),
]

for app in settings.INSTALLED_APPS:
    if app.startswith('collectivo.'):
        pattern = path('', include(f'{app}.urls'))
        urlpatterns.append(pattern)

if settings.DEBUG:

    urlpatterns += [
        # Access static files
        re_path(r'^static/(?P<path>.*)$', serve),

    ]
