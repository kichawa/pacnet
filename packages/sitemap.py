from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.comments.models import Comment
from django.contrib.sitemaps import Sitemap
from django.views.generic.list_detail import object_list

from packages.models import Package, Category

class PackageSitemap(Sitemap):
	changefreq = "weekly"
	priority = 0.5

	def items(self):
		return Package.objects.all()
		
	def location(self, obj):
		return "/package/%s/" % obj.name

		
class CategorySitemap(Sitemap):
	changefreq = "weekly"
	priority = 0.5

	def items(self):
		return Category.objects.all()
		
	def location(self, obj):
		return "/category/%s/" % obj.name

sitemaps = {
	'package': PackageSitemap,
	'category': CategorySitemap,
}
