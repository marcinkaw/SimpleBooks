"""
Definition of urls for Books.
"""

from datetime import datetime
from django.conf.urls import patterns, url
from app.forms import BootstrapAuthenticationForm

from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'app.views.home', name='home'),
    url(r'^contact$', 'app.views.contact', name='contact'),
    url(r'^about', 'app.views.about', name='about'),
    url(r'^login/$',
        'django.contrib.auth.views.login',
        {
            'template_name': 'app/login.html',
            'authentication_form': BootstrapAuthenticationForm,
            'extra_context':
            {
                'title':'Log in',
                'year':datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        'django.contrib.auth.views.logout',
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls), name='admin'),

    url(r'^report/delete/(?P<pk>\d+)/$', 'app.views.report_delete', name='report_delete'),
    url(r'^report/detail/(?P<pk>\d+)/$', 'app.views.report_detail', name='report_detail'),
    url(r'^report/edit/(?P<pk>\d+)/$', 'app.views.report_edit', name='report_edit'),
    url(r'^report/add/$', 'app.views.report_add', name='report_add'),
)
