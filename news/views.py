from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from django.shortcuts import redirect
from slugify import slugify


def news(request):
    return render(request, 'news.html', {'news': 'active'})
