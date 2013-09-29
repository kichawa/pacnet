# -*- coding: utf-8 -*-

from django import forms

from models import Category, Package


class CategoryForm(forms.ModelForm):	
	class Meta:
		model=Category


class PackageForm(forms.ModelForm):	
	class Meta:
		model=Package
		

class PackageCategoryForm(forms.ModelForm):	
	class Meta:
		model=Package
		exclude = ('name','version','www','changelog','description','arch','repo','insert_time','update_time')
