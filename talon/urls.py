"""
Main url router.
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from rest_framework.routers import DefaultRouter
from talon.views import TodoViewSet


# Routers provide an easy way of automatically determining the URL conf
router = DefaultRouter()
router.register(r'todo', TodoViewSet)


urlpatterns = patterns('talon.views',
    # Two step registration
    (r'^accounts/', include('registration.backends.default.urls')),
    # One step registration
    #(r'^accounts/', include('registration.backends.simple.urls')),

    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^oauth2/', include('provider.oauth2.urls', namespace='oauth2')),
    url(r'^ping$', 'ping', name='ping'),
    url(r'^dashboard$', 'dashboard', name='dashboard'),
    url(r'^$', 'index', name='index'),
    url(r'^admin/', include(admin.site.urls)),
)
