from django.contrib.sitemaps import Sitemap

from landing.models import Item

class TodoSitemap(Sitemap):
	changefreq = 'weekly'
	priority = 0.5
	
	def items(self):
		return Item.objects.all()
