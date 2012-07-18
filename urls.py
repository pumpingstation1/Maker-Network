from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^project/', include('project.foo.urls')),
    (r'^accounts/', include('registration.urls')),
    (r'^messages/', include('django.contrib.comments.urls')),


    url(r'^$', 'tagmail.views.home', name='home'),
    url(r'^view_thread/(?P<pk>\d*)/(?P<slug>[\w-]*)$', 'tagmail.views.view_thread', name='tagmail_view_thread'),
    
    url(r'^profile/edit$', 'general.views.edit_profile', name='profile_edit'),
    url(r'^profile/(?P<username>.*)$', 'general.views.view_profile', name='profile_view'),
    url(r'^workinggroup/(?P<id>.*)$', 'general.views.view_workinggroup', name='workinggroup_view'),
    url(r'^groups/', include('general.org_urls')),
    url(r'^skill/', include('general.skill_urls')),
    url(r'^resources/', include('general.resource_urls')),
    url(r'^search/', 'general.views.search', name='search_results'),

    #url(r'^api/', include('api.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

if getattr(settings, 'MEDIA_SERVE', False):
    urlpatterns = patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    ) + urlpatterns

