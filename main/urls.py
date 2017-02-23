from main import views
from django.conf.urls import include, url
from datetime import datetime
from main.forms import BootstrapAuthenticationForm
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^contact$', views.contact, name='contact'),
    url(r'^about', views.about, name='about'),
    url(r'^report/delete/(?P<pk>\d+)/$', views.report_delete, name='report_delete'),
    url(r'^report/detail/(?P<pk>\d+)/$', views.report_detail, name='report_detail'),
    url(r'^report/edit/(?P<pk>\d+)/$', views.report_edit, name='report_edit'),
    url(r'^report/print/(?P<pk>\d+)/$', views.report_print, name='report_print'),
    url(r'^report/add/$', views.report_add, name='report_add'),
    url(r'^item/add/(?P<rpk>\d+)/$', views.item_add, name='item_add'),
    url(r'^item/delete/(?P<rpk>\d+)/(?P<pk>\d+)/$', views.item_delete, name='item_delete'),
    url(r'^api/get_partys/', views.get_partys, name='get_partys'),

    url(r'^login/$',
        auth_views.login,
        {
            'template_name': 'main/login.html',
            'authentication_form': BootstrapAuthenticationForm,
            'extra_context':
            {
              'title':'Log in',
              'year':datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout/$',
        auth_views.logout,
        {
            'next_page': '/main',
        },
        name='logout'),

    # # Uncomment the admin/doc line below to enable admin documentation:
    # # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # #url(r'^admin/', include(admin.site.urls), name='admin'),


    
]
