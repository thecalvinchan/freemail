from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import settings

from freemail import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'freemail.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^sendConf/(?P<email>\w+)', views.sendConf, name='sendConf'),
    url(r'^confirm/(?P<email>\w+)/(?P<hashed>\w+)', views.confirm, name='confirm'),
    url(r'^new_user/(?P<gmail>\w+)/(?P<fb>\w+)', views.addUser, name='addUser'),
    url(r'^getAllUsers$', views.getAllUsers, name='getAllUsers'),
    #serves all other static files

    # url(r'^(?P<path>css/\w+.css)$', views.testPath, name = 'testPath'),
    url(r'^(?P<path>((\w|\-)+\/)*((\w|\-)+\.)+(\w|\-)+)$', 'django.views.static.serve', {'document_root': 'public'}),
    url(r'', views.index, name='index'),
    #url(r'^(?P<path>js/\w+.js)$', 'django.views.static.serve', {'document_root': 'public'}),
    # url(r'^(?P<path>\.css)$', 'django.views.static.serve', {'document_root': '/public'}),
    # url(r'^(?P<path>\.js)$', 'django.views.static.serve', {'document_root': '/public'}),
)
