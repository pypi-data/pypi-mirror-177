"""URL patterns of the extensions module."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'collectivo.extensions'

router = DefaultRouter()
router.register('extensions', views.ExtensionViewSet)

urlpatterns = [
    path('api/extensions/v1/', include(router.urls))
]
