# -*- coding: utf-8 -*-

from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings


class Category(models.Model):
	""" Category model """
	
	name = models.CharField(max_length=20, verbose_name="Nazwa")
	description = models.CharField(max_length=300, verbose_name="Opis", blank=True, null=True)
	
	def __unicode__(self):
		return u"%s" % self.name
		
	def get_absolute_url(self):
		return reverse('category', args=[self.name])
	
	class Meta:
		verbose_name="Kategoria"
		verbose_name_plural="Kategorie"
		ordering = ['name']


class Package(models.Model):
	""" Package model """
	
	ARCH_CHOICES = (
		('i686','i686'),
		('x86_64','x86_64'),
	)
	
	REPO_CHOICES = (
		('core','core'),
		('extra','extra'),
		('testing','testing'),
	)
	
	name = models.CharField(max_length=70, verbose_name="Name")
	category =  models.ForeignKey(Category)
	version = models.CharField(max_length=30, verbose_name="Wersion")
	www = models.CharField(max_length=150, verbose_name="Home site")
	changelog = models.CharField(max_length=100, verbose_name="Changelog")
	description = models.TextField(verbose_name="Description")
	arch = models.CharField(max_length=6, verbose_name='Arch', choices=ARCH_CHOICES)
	repo = models.CharField(max_length=7, verbose_name='Repository', choices=REPO_CHOICES)
	insert_time = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Insert date")
	update_time = models.DateTimeField(editable=False, verbose_name="Update date")
	
	def __unicode__(self):
		return u"%s" % self.name
		
	def get_absolute_url(self):
		return reverse('package', args=[self.name])
		
	
	class Meta:
		verbose_name="Package"
		verbose_name_plural="Packages"
		ordering = ('name',)
		

class PackageHistory(models.Model):
	""" History of category edit """
	
	package =  models.CharField(max_length=70, verbose_name="Package")
	category_from =  models.CharField(max_length=20, verbose_name="From")
	category_to =  models.CharField(max_length=20, verbose_name="To")
	insert_time = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Insert date")
	
	def __unicode__(self):
		return u"%s" % self.package
	
	class Meta:
		verbose_name="Package history"
		verbose_name_plural="Packages history"

