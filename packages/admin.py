# -*- coding: utf-8 -*-

from django.contrib import admin

from models import Category, Package, PackageHistory


class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name',)
	search_fields = ['name',]
	ordering = ['name']

admin.site.register(Category, CategoryAdmin)


class PackageAdmin(admin.ModelAdmin):
	list_display = ('name','category')
	search_fields = ['name','category']
	list_filter = ['category']
	ordering = ['name']

admin.site.register(Package, PackageAdmin)


class PackageHistoryAdmin(admin.ModelAdmin):
	list_display = ('package','category_from','category_to','insert_time')
	search_fields = ['package','category_form','category_to']
	ordering = ['-insert_time']

admin.site.register(PackageHistory, PackageHistoryAdmin)
