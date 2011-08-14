# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^story/page/(?P<page_id>\d+)/$', 'story.views.page'),
    #reset une page
    url(r'^story/page/(?P<page_id>\d+)/reset/$', 'story.views.reset'),
    url(r'^story/page/\d+/(?P<piste_id>\d+)/$', 'story.views.recit'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)
