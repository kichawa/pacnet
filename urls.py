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
	
    url(r'^history/$', 'packages.views.history', name='history'),
	
    url(r'^category/$', 'packages.views.categories', name='categories'),
	url(r'^category/(?P<category_name>[a-zA-Z0-9-]+)/$', 'packages.views.category', name='category'),
	
	url(r'^package/(?P<package_name>[a-zA-Z0-9._+-@]+)/$', 'packages.views.package', name='package'),
	url(r'^change-category/$', 'packages.views.change_category', name='package-category-change'),
	
	url(r'^new-packages/$', 'packages.views.new_packages', name='new-packages'),
	
	url(r'^search/$', 'packages.views.package_search', name='search'),
	
	(r'^api/tosync/', 'packages.views.api_to_sync'),
	(r'^api/categories/', 'packages.views.api_categories'),
	(r'^api/packages/', 'packages.views.api_packages'),
	(r'^api/category/(?P<category_name>[a-zA-Z0-9-]+)/$', 'packages.views.api_category'),
	(r'^api/package/(?P<package_name>[a-zA-Z0-9-@]+)/$', 'packages.views.api_package'),
	(r'^api/search/(?P<search>[a-zA-Z0-9-@]+)/$', 'packages.views.api_search'),
	(r'^api/$', 'packages.views.api'),
    
    (r'^/?$', 'packages.views.main_page'),
)


if settings.DEBUG:
	urlpatterns += patterns('',
		url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {
			'document_root': settings.STATIC_ROOT,
		}),
   )
