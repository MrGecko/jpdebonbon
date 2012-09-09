# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
import settings

slug_pattern = "[A-Za-z0-9]+(-[A-Za-z0-9]+)*"

urlpatterns = patterns('',
      
    url(r'^$', "story.views.home"),
                 
    url(r'^home/$', "story.views.home"), #'django.contrib.auth.views.login', {'template_name': 'story/home.html'}),
    url(r'^home/login/$', "story.views.login"),
    url(r'^home/logout/$', 'django.contrib.auth.views.logout', { "next_page" : "/home/"}),

    #afficher une page
    url(r'^story/(?P<titre_url>%s)/$' % slug_pattern, 'story.views.page'),
    #suivre une piste et obtenir le recit de destination
    url(r'^story/(?P<titre_url>%s)/(?P<piste_id>\d+)/$' % slug_pattern, 'story.views.recit'),
    url(r'^story/(?P<titre_url>%s)/description/$' % slug_pattern, 'story.views.premiere_description'),
    
    url(r'^story/(?P<titre_url>%s)/reset/$' % slug_pattern, 'story.views.reset'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    #ckeditor is a WYSIWYG editor
    (r'^ckeditor/', include('ckeditor.urls')),
    
)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
    (r'^(media|static)/(?P<path>.*)$',
        'serve', {
        'document_root': settings.MEDIA_ROOT,
        'show_indexes': True }),)
    
