from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib import admin

from django.conf import settings
from packages.sitemap import sitemaps

admin.autodiscover()


urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)), 
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	
	(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
	
    (r'^history/$', 'packages.views.history'),
	
    (r'^category/$', 'packages.views.categories'),
	(r'^category/(?P<category_name>[a-zA-Z0-9-]+)/$', 'packages.views.category'),
	
	(r'^package/(?P<package_name>[a-zA-Z0-9._+-]+)/$', 'packages.views.package'),
	(r'^package/(?P<package_name>[a-zA-Z0-9._+-]+)/change-category/$', 'packages.views.change_category'),
	
	(r'^new-packages/$', 'packages.views.new_packages'),
	
	(r'^search/$', 'packages.views.package_search'),
	
	(r'^api/tosync/', 'packages.views.api_to_sync'),
	(r'^api/categories/', 'packages.views.api_categories'),
	(r'^api/packages/', 'packages.views.api_packages'),
	(r'^api/category/(?P<category_name>[a-zA-Z0-9-]+)/$', 'packages.views.api_category'),
	(r'^api/package/(?P<package_name>[a-zA-Z0-9-]+)/$', 'packages.views.api_package'),
	(r'^api/search/(?P<search>[a-zA-Z0-9-]+)/$', 'packages.views.api_search'),
	(r'^api/$', 'packages.views.api'),
    
    
    (r'^/?$', direct_to_template, {'template': 'main-page.html'}),
)


if settings.DEBUG:
	urlpatterns += patterns('',
		url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {
			'document_root': settings.MEDIA_ROOT,
		}),
   )
