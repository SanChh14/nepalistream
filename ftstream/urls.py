"""ftstream URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('matches/', views.matches, name='matches'),
    path('matches/football/', views.football, name='football'),
    path('matches/cricket/', views.cricket, name='cricket'),
    path('matches/football/<slug:slug>/', views.fmatch, name='fmatch'),
    path('matches/cricket/<slug:slug>/', views.cmatch, name='cmatch'),
    path('about/', views.about, name='about'),
    path('contactus/', views.contactus, name='contact'),
    path('privacypolicy/', views.privacypolicy, name='privacy'),
    path('termsandconditions/', views.termsandconditions, name='terms'),
    path('fixtures/', include('fixtures.urls')),
    path('tables/', include('tables.urls')),
    path('news/', include('news.urls')),
    path('highlights/', include('highlights.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
