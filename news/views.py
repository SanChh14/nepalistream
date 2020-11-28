from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from django.shortcuts import redirect
from slugify import slugify
from fixtures.models import site_views

def news(request):
    site = site_views.objects.get(pk='news')
    site.page_views += 1
    site.save()
    return render(request, 'news.html', {'news': 'active'})
