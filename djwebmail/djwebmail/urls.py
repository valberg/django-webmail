from django.conf.urls import patterns, include, url

from webmail.views import ListMessages, Login

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'djwebmail.views.home', name='home'),
    # url(r'^djwebmail/', include('djwebmail.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (
        r'^$',
        ListMessages.as_view()
    ),
    (
        r'^login/?$',
        Login.as_view(),
    ),

    url(r'^admin/', include(admin.site.urls)),
)
