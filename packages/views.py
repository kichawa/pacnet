# -*- coding: utf-8 -*-

import urllib
import sys
try:
    import json
except ImportError:
    import simplejson as json

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.db.models import Q
from django.core import serializers
from django.views.generic.list_detail import object_list
	
from packages.models import *
from settings import SITE_URL


def main_page(request):
	
	new = Package.objects.all().order_by('-id')[:5]
	random = Package.objects.all().order_by('?')[:5]
	
	return render_to_response('main-page.html', { 
		'new': new,
		'random': random
	}, context_instance=RequestContext(request))
	

def categories(request):
	
	categories = Category.objects.all()
	for a in categories:
		a.section = a.name.split('-')[0]
	
	return render_to_response('packages/categories.html', { 
		'categories': categories 
	}, context_instance=RequestContext(request))
	
	
	
def category(request, category_name):
	
	category = get_object_or_404(Category, name=category_name)
	packages = Package.objects.filter(category=category).order_by('name')
	
	return render_to_response('packages/category.html', { 
		'packages': packages,
		'count': len(packages),
		'category': category 
	}, context_instance=RequestContext(request))



def package(request,package_name):
	
	package = get_object_or_404(Package, name=package_name)
	
	return render_to_response('packages/package.html', { 
		'package': package,
	}, context_instance=RequestContext(request))


def change_category(request,package_name):
	
	package = get_object_or_404(Package,name=package_name)
	category_from = package.category
	if request.method == 'POST':
		form = PackageCategoryForm(request.POST, instance=package)
		
		if form.is_valid():
			form.save()
			try:
				new_category = Category.objects.get(id=request.POST.get('category'))
				history = PackageHistory(
					package = package.name,
					category_from = category_from,
					category_to = new_category.name
				)
				history.save()
			except:
				pass
			return HttpResponseRedirect('/package/%s/' % package_name)
		else:
			return render_to_response('packages/change-category.html', { 
				'form': form,
				'package': package
			}, context_instance=RequestContext(request))
	else:
		
		form = PackageCategoryForm(instance=package)
		
		return render_to_response('packages/change-category.html', { 
			'form': form,
			'package': package
		}, context_instance=RequestContext(request))


def new_packages(request):
	
	packages = Package.objects.all().order_by('-id')[:30]
	
	return render_to_response('packages/new-packages.html', { 
		'packages': packages
	}, context_instance=RequestContext(request))


def package_search(request):
	
	if request.method == 'POST':
		search = request.POST.get('search')
		if len(search) < 3:
			return render_to_response('packages/search.html', { 
			'len_error': True,
			'search' : search
			}, context_instance=RequestContext(request))
		else:
			result_name = Package.objects.filter(name__icontains=search)
			result_description = Package.objects.filter(description__icontains=search)
			return render_to_response('packages/search.html', { 
				'result_name': result_name,
				'result_description': result_description,
				'search' : search
			}, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')
		

def history(request):
	
	history = PackageHistory.objects.all().order_by('-insert_time')
	current_page = int(request.GET.get('page', 1))
	
	return object_list(request, history, paginate_by=30, extra_context={ 'current_page' : current_page }, template_name='packages/history.html')


def api(request):
	return render_to_response('packages/api.html', { 'site_url': SITE_URL },  context_instance=RequestContext(request))


def api_to_sync(request):
	
	packages = Package.objects.all().order_by('id')
	
	out = []
	for p in packages:
		out.append({
			'id': p.id,
			'name': p.name,
			'version': p.version
		})
		
	return HttpResponse(json.dumps(out), mimetype="text/javascript")

def api_categories(request):
	
	data = Category.objects.all().order_by('name')
	json = serializers.serialize("json", data)
	
	return HttpResponse(json, mimetype="text/javascript")
	
	
def api_packages(request):
	
	data = Package.objects.all().order_by('name').values('name','version','description','category__name')
	data = list(data)
	json = simplejson.dumps(data)
	
	return HttpResponse(json, mimetype="text/javascript")
	
	
def api_category(request,category_name):
	
	data = Package.objects.filter(category__name=category_name).order_by('name').values('name','version','description')
	data = list(data)
	
	json = simplejson.dumps(data)
	
	return HttpResponse(json, mimetype="text/javascript")
	
	
def api_package(request,package_name):
	
	data = Package.objects.get(name=package_name)
	data = {
		'name': data.name,
		'description': data.description,
		'version' : data.version,
		'www' : data.www,
		'category__name': data.category.name,
		'screenshots' : []
	}
	
	json = simplejson.dumps(data)
	
	return HttpResponse(json, mimetype="text/javascript")


def api_search(request, search):
	
	if len(search) < 3:
		return HttpResponse('{"error": "Need more that 3 chars"}', mimetype="text/javascript")
	else:
		data = Package.objects.filter(Q(name__icontains=search) | Q(description__icontains=search)).values('name','version','description','category__name')
		data = list(data)
		
		json = simplejson.dumps(data)
		
		return HttpResponse(json, mimetype="text/javascript")
