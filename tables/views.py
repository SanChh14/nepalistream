from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from django.shortcuts import redirect
from slugify import slugify


def tables(request):
    return render(request, 'tables.html', {'tables': 'active'})
