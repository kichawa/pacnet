#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyalpm
import os
import json
import urllib.request
import shlex, subprocess

from pyquery import PyQuery as pq


class Pacnet(object):
	
	def __init__(self):
		''' Initialize pyalpm '''
		
		self.pyalpm = pyalpm
		self.pyalpm.initialize()
		self.pyalpm.options.root = "/"
		self.pyalpm.options.dbpath = "/var/lib/pacman"
		self.localdb = self.pyalpm.get_localdb()

		# delete old SQL file if exist	
		if os.path.isfile("update.sql"):
			os.remove("update.sql")
	
	
	def pacnet_db(self):
		''' Get versions of packages from pacnet database '''
		
		#~ result = urllib.request.urlopen("http://pacnet.archlinux.pl/api/tosync/").read()
		result = urllib.request.urlopen("http://pacnet.archlinux.pl/api/tosync/").read()
		packages = json.loads(result.decode('utf-8'))

		package_dict = {}
		for pkg in packages:
			# creating new dictionary with package name as key
			# format: 'epdfview': {'id': 4138, 'version': '0.13.49-2'}
			package_dict[pkg['name']] = {'id': pkg['id'], 'version': pkg['version']}

		return package_dict
	
	
	def pacman_db(self):
		''' Get versions of packages from pacman database '''
		
		self.pyalpm.register_syncdb("core")
		self.pyalpm.register_syncdb("extra")
		self.pyalpm.register_syncdb("community")
		self.repos = self.pyalpm.get_syncdbs()
		
		package_dict = {}
		
		# search packages in all repos
		for repo in self.repos:
			for pkg in repo.pkgcache:
				# creating new dictionary with package name as key
				# format: 'epdfview': {'version': '0.13.49-2'}
				package_dict[pkg.name] = {'version': pkg.version}
			
		return package_dict
	
	
	def addslashes(self,s):
		''' Escaping quotes in SQL '''
		
		return repr('"' + s)[2:-1].replace('"', '\\"') 
	
	
	def changelog(self,package):
		''' Search for package changelog at http://freshmeat.net/ '''

		try:
			html = pq(url="http://freshmeat.net/projects/%s" % package)
		except:
			return False
		title = html('title').text().split(' | ')[0]
		if title == package.upper() or title == package.lower():
			changelog_link = html('.changelog a').attr('href')
			if changelog_link:
				changelog_link = "http://freshmeat.net%s" % changelog_link
				print("\t\033[35m-> changelog: %s\033[0m" % changelog_link)
				self.log("UPDATE packages_package SET changelog='%s' WHERE name='%s'" % (changelog_link,package))

		return False


	def portage(self, package):
		''' Search for package category at http://gentoo-portage.com/ '''
		
		category = "No"
		
		try:
			html = pq(url="http://gentoo-portage.com/Search?search=%s" % package)
			if len(html('#search_results a')) != 0:
				category = html('#search_results a').attr('href').split('/')[1]
		except:
			pass
			
		return category


	def insert(self, package, version):
		''' Generete SQL insert command '''

		# search for package
		for repo in self.repos:
			pkg = repo.get_pkg(package)
			if pkg:
				break
		desc = self.addslashes(pkg.desc)
		try:
			url = pkg.url
		except:
			url = ''
			
		# find portage category in portage
		portage = self.portage(package)

		print("\033[1;31m%s %s [%s]\033[0m" % (package, version, portage))

		# generete SQL INSERT
		self.log("INSERT INTO packages_package (name,category_id,version,www,description,arch,repo,update_time,insert_time,changelog) VALUES ('"+package+"',(SELECT id FROM packages_category WHERE name='"+portage+"'), '"+version+"', '"+url+"', E'"+desc+"','i686','', NOW(),NOW(),'')")

		# find changelog
		self.changelog(package)
			
		
	def update(self, package, pacman_version, id, pacnet_version):
		''' Generete SQL update command '''
		
		# search for package
		for repo in self.repos:
			pkg = repo.get_pkg(package)
			if pkg:
				break
		desc = self.addslashes(pkg.desc)
		
		try:
			url = pkg.url
		except:
			url = ''

		print("%s \033[34m%s\033[0m \033[33m=>\033[0m \033[32m%s\033[0m www: %s" % (package, pacnet_version, pacman_version, url))
		
		# generete SQL UPDATE
		self.log("UPDATE packages_package SET description=E'"+desc+"', www=E'"+url+"', version='"+str(pacman_version)+"' WHERE id='"+str(id)+"'")
		
		# find changelog
		self.changelog(package)
		
		
	def log(self,sql):
		''' Create SQL file '''
		
		logfile = open('update.sql', 'a+')
		logfile.write("%s;\n" % sql)
		logfile.close()


	def delete(self, name):
		''' Delete package from database '''
		
		self.log("DELETE FROM packages_package WHERE name='%s'" % name)


if __name__ == '__main__':
	
	app = Pacnet()
	
	# get both dictionaries
	pacnet = app.pacnet_db()
	pacman = app.pacman_db()

	# version check
	for pkg in pacman:
		try:
			if pacman[pkg]['version'] != pacnet[pkg]['version']:
				# update package
				version = pacman[pkg]['version'];
				id = pacnet[pkg]['id'];
				app.update(pkg, version, id, pacnet[pkg]['version'])
		except:
				# new package
				version = pacman[pkg]['version'];
				app.insert(pkg, version)
				
	# search for deleted packages
	for pkg in pacnet:
		if pkg not in pacman:
			print("\033[1;33m%s\033[0m" % pkg)
			app.delete(pkg)
			
	print("Sending file to server...")
	# you need to create your own script to handle updating database
	command = ["/bin/sh","update.sh"] 
	out, errors = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
	if errors:
		print('[E] Error while sending SQL file')

	print("Done")

