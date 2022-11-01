# sitemaps.py
from django.contrib import sitemaps
from django.urls import reverse

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.7
    changefreq = 'daily'

    def items(self):
        return ['index', 'books', 'books_offers', 'books_requests', 'categories', 'search', 'how_it_works', 'contact_us', 'login', 'register',]

    def location(self, item):
        return reverse(item)